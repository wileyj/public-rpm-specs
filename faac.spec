Name:           faac
Version:        1.28
Release:        1.%{dist}
Summary:        Encoder and encoding library for MPEG2/4 AAC
Group:          Applications/Multimedia
License:        LGPLv2+
Vendor: %{vendor}
Packager: %{packager}
URL:            http://www.audiocoding.com/
Source0:        http://downloads.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.bz2
Patch0:         %{name}-libmp4v2.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libmp4v2-devel


%description
FAAC is an AAC audio encoder. It currently supports MPEG-4 LTP, MAIN and LOW
COMPLEXITY object types and MAIN and LOW MPEG-2 object types. It also supports
multichannel and gapless encoding.

%package devel
Summary:        Development libraries of the FAAC AAC encoder
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
FAAC is an AAC audio encoder. It currently supports MPEG-4 LTP, MAIN and LOW
COMPLEXITY object types and MAIN and LOW MPEG-2 object types. It also supports
multichannel and gapless encoding.

This package contains development files and documentation for libfaac.

%prep
%setup -q
%patch0 -p1 -b .mp4v2
touch -r configure.in.mp4v2 configure.in
#fix permissions
find . -type f \( -name \*.h -or -name \*.c \) -exec chmod 644 {} \;
chmod 644 AUTHORS COPYING ChangeLog NEWS README TODO docs/*

#fix encoding
/usr/bin/iconv -f iso8859-1 -t utf-8 AUTHORS > AUTHORS.conv && touch -r AUTHORS AUTHORS.conv && /bin/mv -f AUTHORS.conv AUTHORS

%build
%configure --disable-static
# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files 
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README TODO docs/*
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/%{name}*

%files devel
%defattr(-,root,root,-)
%exclude  %{_libdir}/*.la
%{_libdir}/*.so
%{_includedir}/*.h

%changelog
