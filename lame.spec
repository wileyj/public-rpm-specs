Name:           lame
Version:        3.99.5
Release:        1.%{dist}
Summary:        Free MP3 audio compressor
Group:          Applications/Multimedia
License:        GPLv2+
Vendor: %{vendor}
Packager: %{packager}
URL:            http://lame.sourceforge.net/
Source0:        http://downloads.sourceforge.net/lame/%{name}-%{version}.tar.gz
#Patch0:         %{name}-as-needed.patch
#Patch1:         %{name}-noexecstack.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  autoconf

BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  libtool-ltdl
BuildRequires:  libtool-ltdl-devel
BuildRequires:  ncurses-devel
#BuildRequires:  gtk+-devel
# pkg-config should be pulled in by gtk+-devel but is not in EL-5
BuildRequires:  pkgconfig
%ifarch %{ix86}
BuildRequires:  nasm
BuildRequires:  gcc >= 3.2
%endif
Requires:       ncurses >= 5.0
Requires:       %{name}-libs = %{version}-%{release}

%description
LAME is an open source MP3 encoder whose quality and speed matches
commercial encoders. LAME handles MPEG1,2 and 2.5 layer III encoding
with both constant and variable bitrates.

%package        libs
Summary:        LAME MP3 encoding library
Group:          System Environment/Libraries

%description    libs
LAME MP3 encoding library.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}

%description    devel
This package development files for %{name}.

%prep
%setup -q -n %{name}-%{version}

#%patch0 -p1 -b .as-needed
#%patch1 -p1 -b .noexec
iconv -f ISO-8859-1 -t UTF8 ChangeLog > ChangeLog.tmp && mv ChangeLog.tmp ChangeLog


%build
#autoreconf
sed -i -e 's/^\(\s*hardcode_libdir_flag_spec\s*=\).*/\1/' configure
%ifarch %{ix86}
export CFLAGS="-fPIC -O3 -mfpmath=sse -m128bit-long-double -mno-align-stringops -minline-all-stringops -m64 -fstack-protector --param=ssp-buffer-size=4 -pipe -D_FORTIFY_
SOURCE=2 -fexceptions " 
export FFLAGS="-fPIC -O3 -mfpmath=sse -m128bit-long-double -mno-align-stringops -minline-all-stringops -m64 -fstack-protector --param=ssp-buffer-size=4 -pipe -D_FORTIFY_
SOURCE=2 -fexceptions "
export CXXFLAGS="-fPIC -O3 -mfpmath=sse -m128bit-long-double -mno-align-stringops -minline-all-stringops -m64 -fstack-protector --param=ssp-buffer-size=4 -pipe -D_FORTIF
Y_SOURCE=2 -fexceptions "
%endif
%configure \
  --disable-dependency-tracking \
  --disable-static \
%ifarch %{ix86}
  --enable-nasm \
%endif
  --enable-mp3rtp \
  --enable-decode-layer1

#automake
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# Some apps still expect to find <lame.h>
ln -sf lame/lame.h $RPM_BUILD_ROOT%{_includedir}/lame.h
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

 
%check
make test


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr (-,root,root,-)
%{_bindir}/lame
%{_bindir}/mp3rtp
%{_mandir}/man1/lame.1*

%files libs
%defattr(-,root,root,-)
%{_libdir}/libmp3lame.so.*

%files devel
%defattr (-,root,root,-)
%{_libdir}/libmp3lame.so
%{_includedir}/lame/
%{_includedir}/lame.h

%changelog
