%{!?cmake_build:%global cmake_build %make_build; cd ..;}
%{!?%cmake_install:%global cmake_install %make_install -C build}

%global with_snapshot 0
%global commit 34da2d23bbf32abf44da11d2cdca595dc7318cec
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:		ispc
Version:	1.14.0	
%if %{with_snapshot}
Release:	20190305.%{shortcommit}
%else
Release:	%mkrel 1
%endif
Summary:	C-based SPMD programming language compiler
Group:		Development/C
License:	BSD
URL:		https://ispc.github.io/
%if %{with_snapshot}
Source0:	https://github.com/%{name}/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:	https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:	bison
BuildRequires:	cmake
BuildRequires:	clang-devel
BuildRequires:	doxygen
BuildRequires:	flex
BuildRequires:	git
BuildRequires:	gcc-c++
BuildRequires:	llvm-devel
BuildRequires:	rst2html
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(zlib)

# Exlcude architectures failing to build
ExclusiveArch:	x86_64 aarch64

# https://fedoraproject.org/wiki/Changes/Stop-Shipping-Individual-Component-Libraries-In-clang-lib-Package
Patch0:	0001-Link-against-libclang-cpp.so.patch

#
# Fix examples path
# From git
Patch109:	0109-Fix-for-1844-backport-of-LLVM-patch.patch
Patch110:	0110-Triger-LLVM-rebuild-not-only-in-master.patch
Patch111:	0111-Rebuild-LLVM-with-and-without-asserts-enabled.patch
Patch112:	0112-Adjust-fix-1844-run-only-for-10.0-and-generate-objec.patch

#
Patch200:	ispc-1.11.0-examples-path.patch
Patch201:	ispc-1.13.0-remove-unused-variables.patch
Patch202:	ispc-1.13.0-remove-unsupported-flags.patch

%description
A compiler for a variant of the C programming language, with extensions for
"single program, multiple data" (SPMD) programming.

%package examples
Summary:        Examples binaries for ispc
Group:          Development/C

%description examples
This package contains the examples binaries for the ispc SPMD compiler.

%prep
%if %{with_snapshot}
%setup -n %{name}-%{commit}
%else
%setup
%endif
%patch109 -p1
%patch110 -p1
%patch111 -p1
%patch112 -p1
%patch200 -p1 -b .examples
%patch201 -p1 -b .unused
%patch202 -p1 -b .unsupport
%if %{mgaversion} >= 8
%patch0 -p1 -b .clang
%endif

# Use gcc rather clang by default
sed -i 's|set(CMAKE_C_COMPILER "clang")|set(CMAKE_C_COMPILER "gcc")|g' CMakeLists.txt
sed -i 's|set(CMAKE_CXX_COMPILER "clang++")|set(CMAKE_CXX_COMPILER "g++")|g' CMakeLists.txt

# Delete unrecognized command options from gcc-c++
sed -i 's|-Wno-c99-extensions -Wno-deprecated-register||g' CMakeLists.txt

# Suppress warning message as error
sed -i 's| -Werror ||g' CMakeLists.txt 

# Fix all Python shebangs recursively in .
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" .

%build
%cmake	\
	-DCMAKE_EXE_LINKER_FLAGS:STRING="%{optflags} -fPIE" \
	-DISPC_INCLUDE_EXAMPLES=ON \
	-DISPC_INCLUDE_TESTS=OFF \
	-DISPC_NO_DUMPS=ON \
	.
	
%cmake_build

(
 cd ./docs/
 ./build.sh
)

%install
mkdir -p %{buildroot}%{_libdir}/ispc
%cmake_install

%files
%license LICENSE.txt
%doc docs/*.html docs/ReleaseNotes.txt
%{_bindir}/%{name}
%{_bindir}/check_isa

%files examples
%{_prefix}/lib/ispc/examples
