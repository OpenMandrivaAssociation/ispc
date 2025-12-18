%define major 1
%define minor 29
%define libname %mklibname ispc
%define devname %mklibname ispc -d
%define static %mklibname ispc-static -d

Name:		ispc
Version:	1.29.0
Release:	2
Summary:	C-based SPMD programming language compiler
Group:		Development/C
License:	BSD-3-Clause
URL:		https://ispc.github.io/
Source0:	https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:	bison
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	clang-devel
BuildRequires:	doxygen
BuildRequires:	flex
BuildRequires:	git
BuildRequires:	gcc-c++
BuildRequires:	llvm-devel
BuildRequires:	python%{pyver}dist(docutils)
BuildRequires:	python%{pyver}dist(pygments)
BuildRequires:	pkgconfig(gtest)
BuildRequires:	pkgconfig(gmock)
# intel oneapi level zero devel package
BuildRequires:	pkgconfig(level-zero)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(python)
BuildRequires:  pkgconfig(tbb)
BuildRequires:	%{_lib}tbbind
BuildRequires:	pkgconfig(zlib)

Requires:	%{libname} = %{version}-%{release}

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
Requires:	%{name} = %{version}-%{release}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

##############################
%package	-n %{static}
Summary:	Static libraries for %{name} development
Requires:	%{devname} = %{version}-%{release}

%description -n %{static}
The %{static} package includes static libraries needed
to develop programs that use %{name}.

##############################

%prep
%autosetup -p1

# Remove git badge remote images from README
sed -i '1,13d;134d;' README.md

%cmake	\
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_C_FLAGS:STRING="$CFLAGS %{optflags} -fPIE" \
	-DCMAKE_CXX_FLAGS:STRING="$CXXFLAGS %{optflags} -fPIE" \
	-DCMAKE_EXE_LINKER_FLAGS:STRING="%{optflags} -fPIE" \
	-DCURSES_CURSES_LIBRARY=%{_libdir}/libncurses.so \
	-DISPC_INCLUDE_EXAMPLES=OFF \
	-DISPC_INCLUDE_TESTS=ON \
	-DISPCRT_BUILD_CPU=ON \
	-DISPCRT_BUILD_GPU=ON \
	-DISPCRT_BUILD_TESTS=OFF \
	-DRISCV_ENABLED=ON \
	-G Ninja

	# Removed option as it requires LLVM patching and the CMake LLVMGenXIntrinsicsPath
	# variable to be populated.
	#-DXE_ENABLED=ON \
%build
%ninja_build -C build

# build docs
(
 cd ./docs/
 ./build.sh
)


%install
%ninja_install -C build

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

