%define major 1
%define minor 30
%define libname %mklibname ispc
%define devname %mklibname ispc -d
%define static %mklibname ispc-static -d

Name:		ispc
Version:	1.30.0
Release:	2
Summary:	C-based SPMD programming language compiler
Group:		Development/C
License:	BSD-3-Clause
URL:		https://ispc.github.io/
Source0:	https://github.com/ispc/ispc/archive/v%{version}/%{name}-%{version}.tar.gz
# repo - https://github.com/ispc/ispc

BuildSystem:	cmake
BuildOption(prep):	-p1
BuildOption:	-DCMAKE_INSTALL_PREFIX="%{_prefix}"
BuildOption:	-DCMAKE_C_FLAGS:STRING="$CFLAGS %{optflags} -fPIE"
BuildOption:	-DCMAKE_CXX_FLAGS:STRING="$CXXFLAGS %{optflags} -fPIE"
BuildOption:	-DCMAKE_EXE_LINKER_FLAGS:STRING="%{optflags} -fPIE"
BuildOption:	-DCURSES_CURSES_LIBRARY="%{_libdir}/libncurses.so"
BuildOption:	-DISPC_INCLUDE_EXAMPLES:BOOL=OFF
BuildOption:	-DISPC_INCLUDE_TESTS:BOOL=ON
BuildOption:	-DISPCRT_BUILD_CPU:BOOL=ON
BuildOption:	-DISPCRT_BUILD_GPU:BOOL=ON
BuildOption:	-DISPCRT_BUILD_TESTS:BOOL=OFF
BuildOption:	-DRISCV_ENABLED:BOOL=ON


BuildRequires:	bison
BuildRequires:	cmake
BuildRequires:	cmake(clang)
BuildRequires:	cmake(LLVM)
BuildRequires:	doxygen
BuildRequires:	flex
BuildRequires:	git
BuildRequires:	gcc-c++
BuildRequires:	ninja
BuildRequires:	pkgconfig(gmock)
BuildRequires:	pkgconfig(gtest)
# intel oneapi level zero devel package
BuildRequires:	pkgconfig(level-zero)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(python)
BuildRequires:  pkgconfig(tbb)
BuildRequires:	%{_lib}tbbind
BuildRequires:	pkgconfig(zlib)
BuildRequires:	python%{pyver}dist(docutils)
BuildRequires:	python%{pyver}dist(pygments)

Requires:	%{libname} = %{EVRD}

# Upstream only supports these architectures
# Upstream added experiemental riscv64 support in v1.29.0
ExclusiveArch:	x86_64 aarch64 znver1 riscv64

%description
A compiler for a variant of the C programming language, with extensions for
"single program, multiple data" (SPMD) programming.

##############################
%package -n %{libname}
Summary:	C-based SPMD programming language compiler library for %{name}
Group:		System/Libraries

%description -n %{libname}
Libary for a variant of the C programming language, with extensions for
"single program, multiple data" (SPMD) programming.

##############################
%package -n %{devname}
Summary:	Development files (Headers etc.) for %{name}
Group:		Development/C and C++
Requires:	%{name} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

##############################
%package	-n %{static}
Summary:	Static libraries for %{name} development
Requires:	%{devname} = %{EVRD}

%description -n %{static}
The %{static} package includes static libraries needed
to develop programs that use %{name}.

##############################

%build -a
# build docs
(
 cd ./docs/
 ./build.sh
)

%check
export PATH="${PATH}:%{buildroot}%{_bindir}"
%{__python} scripts/run_tests.py

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files
%{_bindir}/%{name}
%{_bindir}/check_isa
%doc README.md
%doc docs/*.html docs/ReleaseNotes.txt
%license LICENSE.txt

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}
%{_libdir}/lib%{name}.so.%{major}.%{minor}.*
%{_libdir}/lib%{name}rt*.so.%{major}
%{_libdir}/lib%{name}rt*.so.%{major}.%{minor}.*
%license LICENSE.txt
%doc README.md

%files -n %{devname}
%{_includedir}/intrinsics/
%{_includedir}/%{name}/
%{_includedir}/%{name}rt/
%{_includedir}/stdlib/
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}rt*.so
%{_libdir}/cmake/%{name}
%{_libdir}/cmake/%{name}rt-%{version}
%license LICENSE.txt
%doc README.md

%files -n %{static}
%{_libdir}/lib%{name}rt_static.a
%license LICENSE.txt

