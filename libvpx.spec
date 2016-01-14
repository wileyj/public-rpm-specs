%define major 1
%define snapshot 0

# disable to build without php and doxygen
%define build_doc 0

Name:			libvpx
Summary:		VP8 Video Codec SDK
Version:		1.1.0
Release:		1.%{dist}
License:		BSD
Vendor: %{vendor}
Packager: %{packager}
Group:			System/Libraries
Source0:		http://webm.googlecode.com/files/%{name}-v%{version}.tar.bz2
Source2:		libvpx.ver
Patch0:			01_enable-shared.patch
URL:			http://www.webmproject.org/tools/vp8-sdk/
BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root
%ifarch %{ix86} x86_64
BuildRequires:		yasm
%endif
%if %build_doc
BuildRequires:		doxygen, php-cli
%endif

%description
libvpx provides the VP8 SDK, which allows you to integrate your applications 
with the VP8 video codec, a high quality, royalty free, open source codec 
deployed on millions of computers and devices worldwide. 


%package libs
Summary:		VP8 Video Codec SDK
Group:			System/Libraries
Provides:               %{name}-libs = %{version}
%description libs
libvpx provides the VP8 SDK, which allows you to integrate your applications 
with the VP8 video codec, a high quality, royalty free, open source codec 
deployed on millions of computers and devices worldwide. 


%package devel
Summary:		Development files for libvpx
Group:			Development/C
Requires:		%{name}-devel = %{version}-%{release}
Provides: %name-devel = %version-%release

%description devel
Development libraries and headers for developing software against 
libvpx.

%package utils
Summary:		VP8 utilities and tools
Group:			Video/Utilities
Requires:		vpx-libs = %{version}

%description utils
A selection of utilities and tools for VP8, including a sample encoder
and decoder.


%prep
%setup -q -n %{name}-v%{version}

# fix permissions
chmod 644 AUTHORS CHANGELOG LICENSE README
%patch0 -p1  

%build
%ifarch %{ix86}
%global vpxtarget x86-linux-gcc
%else
%ifarch	x86_64
%global	vpxtarget x86_64-linux-gcc
%else
%global vpxtarget generic-gnu
%endif
%endif

# The configure script will reject the shared flag on the generic target
# This means we need to fall back to the manual creation we did before. :P
%if "%{vpxtarget}" == "generic-gnu"
%global generic_target 1
%else
%global generic_target 0
%endif
export CFLAGS="-fPIC -O3 -mfpmath=sse -m128bit-long-double -mno-align-stringops -minline-all-stringops -m64 -fstack-protector --param=ssp-buffer-size=4 -pipe -D_FORTIFY_SOURCE=2 -fexceptions " 
export FFLAGS="-fPIC -O3 -mfpmath=sse -m128bit-long-double -mno-align-stringops -minline-all-stringops -m64 -fstack-protector --param=ssp-buffer-size=4 -pipe -D_FORTIFY_SOURCE=2 -fexceptions "
export CXXFLAGS="-fPIC -O3 -mfpmath=sse -m128bit-long-double -mno-align-stringops -minline-all-stringops -m64 -fstack-protector --param=ssp-buffer-size=4 -pipe -D_FORTIFY_SOURCE=2 -fexceptions "
./configure \
    --target=%{vpxtarget} \
    --enable-pic \
    --disable-install-srcs \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --enable-shared

%{__make} verbose=true target=libs

# Temporarily dance the static libs out of the way
mv libvpx.a libNOTvpx.a
mv libvpx_g.a libNOTvpx_g.a

# We need to do this so the examples can link against it.
ln -sf libvpx.so.%{version} libvpx.so


# Put them back so the install doesn't fail
mv libNOTvpx.a libvpx.a
mv libNOTvpx_g.a libvpx_g.a

%install
make DIST_DIR=%{buildroot}%{_prefix} dist

# Install the pkg-config file
#mkdir -p %{buildroot}%{_libdir}/pkgconfig/
if [ -s %{buildroot}%{_libdir}/pkgconfig/libvpx.pc ]
then
  %__rm %{buildroot}%{_libdir}/pkgconfig/libvpx.pc
fi
ln -s vpx.pc %{buildroot}%{_libdir}/pkgconfig/libvpx.pc


pushd %{buildroot}
# Stuff we don't need.
rm -rf usr/build/ usr/md5sums.txt usr/lib*/*.a usr/CHANGELOG usr/README
# Rename a few examples
mv usr/bin/postproc usr/bin/vp8_postproc
mv usr/bin/simple_decoder usr/bin/vp8_simple_decoder
mv usr/bin/simple_encoder usr/bin/vp8_simple_encoder
mv usr/bin/twopass_encoder usr/bin/vp8_twopass_encoder
# Fix the binary permissions
chmod 755 usr/bin/*
popd

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files libs
%doc AUTHORS CHANGELOG LICENSE README
%{_libdir}/libvpx.so.%{major}*

%files devel
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libvpx.so
# to fix weird header files permissions
%defattr(644,root,root,755)
%{_includedir}/vpx/

%files utils
%{_bindir}/*
