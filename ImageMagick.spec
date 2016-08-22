%global VER 6.9.3
%global Patchlevel 2

%define _installpath /opt/ImageMagick-%{VER}
%define IMbindir %{_installpath}/bin
%define IMsbindir %{_installpath}/sbin
%define IMlibexecdir %{_installpath}/libexec
%define IMlibdir  %{_installpath}/lib
%define IMdatadir  %{_installpath}/share
%define IMincludedir  %{_installpath}/include


Name:		ImageMagick
Version:		%{VER}.%{Patchlevel}
Release:		1.%{dist}
Summary:		An X application for displaying and manipulating images
Group:		Applications/Multimedia
License:		ImageMagick
Vendor: %{vendor}
Packager: %{packager}
Url:			http://www.imagemagick.org/
Source0:		ftp://ftp.ImageMagick.org/pub/%{name}/%{name}-%{VER}-%{Patchlevel}.tar.gz
#Patch0:			PerlMagick-Makefile.patch

Requires:		%{name}-libs = %{version}-%{release}

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	bzip2-devel, freetype-devel, libjpeg-devel, libpng-devel
BuildRequires:	libtiff-devel, giflib-devel, zlib-devel, perl-devel >= 5.8.1
BuildRequires:	ghostscript-devel
#BuildRequires: djvulibre-devel
BuildRequires:	libwmf-devel, jasper-devel, libtool-ltdl-devel
BuildRequires:	libX11-devel, libXext-devel, libXt-devel
BuildRequires:	lcms2-devel, libxml2-devel
#BuildRequires:  librsvg2-devel, OpenEXR-devel
BuildRequires:	fftw-devel, libwebp-devel

%description
ImageMagick is an image display and manipulation tool for the X
Window System. ImageMagick can read and write JPEG, TIFF, PNM, GIF,
and Photo CD image formats. It can resize, rotate, sharpen, color
reduce, or add special effects to an image, and when finished you can
either save the completed work in the original format or a different
one. ImageMagick also includes command line programs for creating
animated or transparent .gifs, creating composite images, creating
thumbnail images, and more.

ImageMagick is one of your choices if you need a program to manipulate
and display images. If you want to develop your own applications
which use ImageMagick code or APIs, you need to install
ImageMagick-devel as well.


%package devel
Summary:	Library links and header files for ImageMagick app development
Group:	Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libX11-devel, libXext-devel, libXt-devel, ghostscript-devel
Requires:	bzip2-devel, freetype-devel, libtiff-devel, libjpeg-devel, lcms2-devel
Requires:	libwebp-devel, jasper-devel, pkgconfig
#Requires:	librsvg, OpenEXR-devel
Requires:	%{name}-libs = %{version}-%{release}

%description devel
ImageMagick-devel contains the library links and header files you'll
need to develop ImageMagick applications. ImageMagick is an image
manipulation program.

If you want to create applications that will use ImageMagick code or
APIs, you need to install ImageMagick-devel as well as ImageMagick.
You do not need to install it if you just want to use ImageMagick,
however.


%package libs
Summary: ImageMagick libraries to link with
Group: Applications/Multimedia

%description libs
This packages contains a shared libraries to use within other applications.


#%package djvu
#Summary: DjVu plugin for ImageMagick
#Group: Applications/Multimedia
#Requires: %{name} = %{version}-%{release}
#
#%description djvu
#This packages contains a plugin for ImageMagick which makes it possible to
#save and load DjvU files from ImageMagick and libMagickCore using applications.


%package doc
Summary: ImageMagick html documentation
Group: Documentation

%description doc
ImageMagick documentation, this package contains usage (for the
commandline tools) and API (for the libraries) documentation in html format.
Note this documentation can also be found on the ImageMagick website:
http://www.imagemagick.org/


%package perl
Summary: ImageMagick perl bindings
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description perl
Perl bindings to ImageMagick.

Install ImageMagick-perl if you want to use any perl scripts that use
ImageMagick.


%package c++
Summary: ImageMagick Magick++ library (C++ bindings)
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description c++
This package contains the Magick++ library, a C++ binding to the ImageMagick
graphics manipulation library.

Install ImageMagick-c++ if you want to use any applications that use Magick++.


%package c++-devel
Summary: C++ bindings for the ImageMagick library
Group: Development/Libraries
Requires: %{name}-c++ = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

%description c++-devel
ImageMagick-devel contains the static libraries and header files you'll
need to develop ImageMagick applications using the Magick++ C++ bindings.
ImageMagick is an image manipulation program.

If you want to create applications that will use Magick++ code
or APIs, you'll need to install ImageMagick-c++-devel, ImageMagick-devel and
ImageMagick.
You don't need to install it if you just want to use ImageMagick, or if you
want to develop/compile applications using the ImageMagick C interface,
however.


%prep
%setup -q -n %{name}-%{VER}-%{Patchlevel}
#%patch0 -p0

#read ans
sed -i 's/libltdl.la/libltdl.so/g' configure
iconv -f ISO-8859-1 -t UTF-8 README.txt > README.txt.tmp
touch -r README.txt README.txt.tmp
mv README.txt.tmp README.txt
# for %%doc
mkdir Magick++/examples
cp -p Magick++/demo/*.cpp Magick++/demo/*.miff Magick++/examples


%build
export CPPFLAGS="-I%{_includedir}/openjpeg-2.1"

%configure \
        --prefix=%{_installpath} \
        --bindir=%{IMbindir} \
        --sbindir=%{IMsbindir} \
        --libexec=%{IMlibexecdir} \
        --sysconfdir=%{_installpath}/etc \
        --libdir=%{IMlibdir} \
        --includedir=%{IMincludedir} \
        --datarootdir=%{IMdatadir} \
        --localstatedir=%{_installpath}/var \
	--enable-shared \
	--disable-static \
	--with-modules \
	--with-perl \
	--with-x \
	--with-threads \
	--with-magick_plus_plus \
	--with-gslib \
	--with-wmf \
	--with-lcms2 \
	--with-webp \
	--with-openexr \
	--with-rsvg \
	--with-xml \
	--with-perl-options="INSTALLDIRS=vendor %{?perl_prefix} CC='%__cc -L$PWD/magick/.libs' LDDLFLAGS='-shared -L$PWD/magick/.libs'" \
	--without-dps \
	--without-included-ltdl --with-ltdl-include=%{IMincludedir} \
	--with-ltdl-lib=%{IMlibdir}

# Disable rpath
sed -i 's|^hardcodeIMlibdir_flag_spec=.*|hardcodeIMlibdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# Do *NOT* use %%{?_smp_mflags}, this causes PerlMagick to be silently misbuild
make


%install
rm -rf %{buildroot}

make %{?_smp_mflags} install DESTDIR=%{buildroot} INSTALL="install -p"
#cp -a www/source %{buildroot}%{IMdatadir}/doc/%{name}-%{VER}
cp -a www/source %{buildroot}%{_datadir}/doc/%{name}-%{VER}
# Delete *ONLY* IMlibdir/*.la files! .la files used internally to handle plugins - BUG#185237!!!
rm %{buildroot}%{IMlibdir}/*.la

# fix weird perl Magick.so permissions
chmod 755 %{buildroot}%{perl_vendorarch}/auto/Image/Magick/Magick.so

# perlmagick: fix perl path of demo files
%{__perl} -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)' PerlMagick/demo/*.pl

# perlmagick: cleanup various perl tempfiles from the build which get installed
find %{buildroot} -name "*.bs" |xargs rm -f
find %{buildroot} -name ".packlist" |xargs rm -f
find %{buildroot} -name "perllocal.pod" |xargs rm -f

# perlmagick: build files list
echo "%defattr(-,root,root,-)" > perl-pkg-files
find %{buildroot}/%{IMlibdir}/perl* -type f -print \
	| sed "s@^%{buildroot}@@g" > perl-pkg-files
find %{buildroot}%{perl_vendorarch} -type d -print \
	| sed "s@^%{buildroot}@%dir @g" \
	| grep -v '^%dir %{perl_vendorarch}$' \
	| grep -v '/auto$' >> perl-pkg-files
find %{buildroot}/%{perl_vendorarch} -type f -print \
	| sed "s@^%{buildroot}@@g" >> perl-pkg-files
if [ -z perl-pkg-files ] ; then
	echo "ERROR: EMPTY FILE LIST"
	exit -1
fi

# fix multilib issues

mv %{buildroot}%{IMincludedir}/%{name}-6/magick/magick-config.h \
	%{buildroot}%{IMincludedir}/%{name}-6/magick/magick-config-%{__isa_bits}.h

cat >%{buildroot}%{IMincludedir}/%{name}-6/magick/magick-config.h <<EOF
#ifndef IMAGEMAGICK_MULTILIB
#define IMAGEMAGICK_MULTILIB

#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "magick-config-32.h"
#elif __WORDSIZE == 64
# include "magick-config-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif

#endif
EOF

# Fonts must be packaged separately. It does nothave matter and demos work without it.
rm PerlMagick/demo/Generic.ttf
mkdir -p %{buildroot}/etc/profile.d
cat <<EOF> %{buildroot}/etc/profile.d/ImageMagick.sh
export PATH=$PATH:%{IMbindir}
EOF
chmod a+x %{buildroot}/etc/profile.d/ImageMagick.sh
#%check
##export LD_LIBRARY_PATH=%{buildroot}/wand/.libs/:%{buildroot}/Magick++/lib/.libs/
#export LD_LIBRARY_PATH=%{buildroot}/%{IMlibdir}
#make %{?_smp_mflags} check

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%post libs -p /sbin/ldconfig

%post c++ -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%postun c++ -p /sbin/ldconfig


%files
%doc README.txt LICENSE NOTICE AUTHORS.txt NEWS.txt ChangeLog Platforms.txt
%{IMbindir}/[a-z]*
/etc/profile.d/ImageMagick.sh
%{_mandir}/man[145]/[a-z]*
%{_mandir}/man1/%{name}.*

%files libs
%defattr(-,root,root,-)
%doc LICENSE NOTICE AUTHORS.txt QuickStart.txt
%{IMlibdir}/libMagickCore-6.Q16.so.2*
%{IMlibdir}/libMagickWand-6.Q16.so.2*
%{IMlibdir}/%{name}-%{VER}
%{_datadir}/%{name}-6
#%exclude %{IMlibdir}/%{name}-%{VER}/modules-Q16/coders/djvu.*
%{_installpath}%{_sysconfdir}/%{name}-6

%files devel
%defattr(-,root,root,-)
%{IMbindir}/MagickCore-config
%{IMbindir}/Magick-config
%{IMbindir}/MagickWand-config
%{IMbindir}/Wand-config
%{IMlibdir}/libMagickCore-6.Q16.so
%{IMlibdir}/libMagickWand-6.Q16.so
%{IMlibdir}/pkgconfig/MagickCore.pc
%{IMlibdir}/pkgconfig/MagickCore-6.Q16.pc
%{IMlibdir}/pkgconfig/ImageMagick.pc
%{IMlibdir}/pkgconfig/ImageMagick-6.Q16.pc
%{IMlibdir}/pkgconfig/MagickWand.pc
%{IMlibdir}/pkgconfig/MagickWand-6.Q16.pc
%{IMlibdir}/pkgconfig/Wand.pc
%{IMlibdir}/pkgconfig/Wand-6.Q16.pc
%dir %{IMincludedir}/%{name}-6
%{IMincludedir}/%{name}-6/magick
%{IMincludedir}/%{name}-6/wand
%{_mandir}/man1/Magick-config.*
%{_mandir}/man1/MagickCore-config.*
%{_mandir}/man1/Wand-config.*
%{_mandir}/man1/MagickWand-config.*

#%files djvu
#%defattr(-,root,root,-)
#%{IMlibdir}/%{name}-%{VER}/modules-Q16/coders/djvu.*

%files doc
%defattr(-,root,root,-)
%doc %{_datadir}/doc/%{name}-6
%doc %{_datadir}/doc/%{name}-%{VER}
%doc LICENSE

%files c++
%defattr(-,root,root,-)
%doc Magick++/AUTHORS Magick++/ChangeLog Magick++/NEWS Magick++/README
%doc www/Magick++/COPYING
%{IMlibdir}/libMagick++-6.Q16.so.*

%files c++-devel
%defattr(-,root,root,-)
%doc Magick++/examples
%{IMbindir}/Magick++-config
%{IMincludedir}/%{name}-6/Magick++
%{IMincludedir}/%{name}-6/Magick++.h
%{IMlibdir}/libMagick++-6.Q16.so
%{IMlibdir}/pkgconfig/Magick++.pc
%{IMlibdir}/pkgconfig/Magick++-6.Q16.pc
%{IMlibdir}/pkgconfig/ImageMagick++.pc
%{IMlibdir}/pkgconfig/ImageMagick++-6.Q16.pc
%{_mandir}/man1/Magick++-config.*

%files perl -f perl-pkg-files
%defattr(-,root,root,-)
%{_mandir}/man3/*
%doc PerlMagick/demo/ PerlMagick/Changelog PerlMagick/README.txt

%changelog
