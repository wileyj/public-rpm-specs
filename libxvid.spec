%define bname xvid
%define Name XviD
%define _smp_mflags -j6 -O2 -g -march=x86_64 -mtune=x86_64

Name: lib%bname
Version: 1.3.2
Release: 1.%{dist}
Summary: Shared library of %Name video codec
Group: System/Libraries
License: GPLv2+
Vendor: %{vendor}
Packager: %{packager}
URL: http://www.%bname.org
Provides: lib%bname = %version-%release
Obsoletes: lib%bname < %version-%release
Source: %{bname}core-%version.tar.gz
BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: nasm

%description
%Name is a high performance and high quality MPEG-4 video de-/encoding
solution.
This package includes the shared library needed to run %Name software.

%package devel
Summary: Development files of %Name video codec
Group: Development/C
Requires: %name = %version-%release
Provides: lib%bname-devel = %version-%release
Obsoletes: lib%bname-devel < %version-%release

%description devel
%Name is a high performance and high quality MPEG-4 video de-/encoding
solution.
This package includes the header files needed to develop %Name-based
software.

%prep
%setup -q -n %{bname}core

%build
export CFLAGS="-fPIC -O3 -mfpmath=sse -m128bit-long-double -mno-align-stringops -minline-all-stringops -m64 -fstack-protector --param=ssp-buffer-size=4 -pipe -D_FORTIFY_SOURCE=2 -fexceptions "
export FFLAGS="-fPIC -O3 -mfpmath=sse -m128bit-long-double -mno-align-stringops -minline-all-stringops -m64 -fstack-protector --param=ssp-buffer-size=4 -pipe -D_FORTIFY_SOURCE=2 -fexceptions "
export CXXFLAGS="-fPIC -O3 -mfpmath=sse -m128bit-long-double -mno-align-stringops -minline-all-stringops -m64 -fstack-protector --param=ssp-buffer-size=4 -pipe -D_FORTIFY_SOURCE=2 -fexceptions "

pushd build/generic
%configure
%{__make} 
popd

%install
pushd build/generic
%{__make} DESTDIR=%buildroot install
popd

ln -s %{name}core.so.4.3 %buildroot%_libdir/%{name}core.so
rm -f %buildroot%_libdir/*.a

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%doc AUTHORS README
%_libdir/*.so.*

%files devel
%_includedir/*
%_libdir/*.so

%changelog
