Name:           libntlm
Version:        1.0
Release:        1.%{dist}
Summary:        NTLM authentication library 
Group:          System Environment/Libraries
License:        LGPLv2+
Vendor: %{vendor}
Packager: %{packager}
URL:            http://josefsson.org/libntlm/
Source0:        http://josefsson.org/libntlm/releases/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  pkgconfig

%description
A library for authenticating with Microsoft NTLM challenge-response,
derived from Samba sources.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
touch -r NEWS $RPM_BUILD_ROOT%{_includedir}/ntlm.h
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README THANKS
%{_libdir}/libntlm.so.*

%files devel
%defattr(-,root,root,-)
%doc COPYING 
%{_includedir}/ntlm.h
%{_libdir}/libntlm.so
%{_libdir}/pkgconfig/libntlm.pc


%changelog
