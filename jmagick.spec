%define repo https://github.com/techblue/jmagick
%define jmagick_version 6.7.7
%define imagemagick_version 6.9.3
%define _installpath /opt/JMagick-%{jmagick_version}
%define _imagemagick /opt/ImageMagick-%{imagemagick_version}
%define _bindir %{_installpath}/bin
%define _sbindir %{_installpath}/sbin
%define _libexecdir %{_installpath}/libexec
%define _libdir  %{_installpath}/lib
%define _datadir  %{_installpath}/share
%define _includedir  %{_installpath}/include
%define pkgconfig  %{_imagemagick}/lib/pkgconfig
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1

Summary: Jmagick - Java interface to ImageMagick 
Name: jmagick
Version: %{jmagick_version}
Release: %{rel_version}.%{revision}.%{dist}
License: LGPL
Vendor: %{vendor}
Packager: %{packager}
Group: Applications/Graphic
BuildRequires:  libopenjpeg-devel ImageMagick-devel ImageMagick jdk pkgconfig freetype-devel, libtiff-devel, libtiff, zlib-devel, libgomp, bzip2-libs, bzip2-devel
Requires: ImageMagick  jdk libtiff-devel libtiff

%description
JMagick is an open source Java interface of ImageMagick. It is implemented in the form of a thin Java Native Interface (JNI) layer into the ImageMagick API.

%setup -q -c -T
%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
#sed -i "s|jar cvf|$JAVA_HOME/bin/jar cvf|g" Makefile
export CPPFLAGS="-I%{_imagemagick}/include"
export LDFLAGS="-L%{_imagemagick}/lib"

%build
cd %{name}-%{version}
./configure --prefix=%{_installpath} \
      --with-magick-home=%{_imagemagick} \
      --with-java-home="$JAVA_HOME" \
      --with-magick-inc-dir=%{_imagemagick}/include/ImageMagick-6 \
      --with-magick-lib-dir=%{_imagemagick}/lib \
      --with-java-home=/usr/java/current \
      PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%{_imagemagick}/lib/pkgconfig
mkdir -p $RPM_BUILD_ROOT/%{_installpath}

%{__make} all
%install
cd %{name}-%{version}
%{__make} DESTDIR=$RPM_BUILD_ROOT install

%post
ln -sf %{_installpath}/lib/libJMagick-%{version}.so %{_installpath}/lib/libJMagick.so
ln -sf %{_installpath}/lib/jmagick-%{version}.jar %{_installpath}/lib/jmagick.jar

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root,-)
%{_installpath}


%changelog
