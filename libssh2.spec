Name:           libssh2
Version:        1.6.0
Release:        1.%{dist}
Summary:        A library implementing the SSH2 protocol
Group:          System Environment/Libraries
License:        BSD
Vendor: %{vendor}
Packager: %{packager}
URL:            http://www.libssh2.org/
Source0:        http://downloads.sourceforge.net/libssh2/%{name}-%{version}.tar.gz

#Patch0:		libssh2-0.18-padding.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  openssl-devel
BuildRequires:  zlib-devel   
BuildRequires:  pkgconfig

%description
libssh2 is a library implementing the SSH2 protocol as defined by
Internet Drafts: SECSH-TRANS(22), SECSH-USERAUTH(25),
SECSH-CONNECTION(23), SECSH-ARCH(20), SECSH-FILEXFER(06)*,
SECSH-DHGEX(04), and SECSH-NUMBERS(10).


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        docs 
Summary:        Documentation for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    docs
The %{name}-docs package contains man pages and examples for
developing applications that use %{name}.


%prep
%setup -q

#%patch0 -p1 -b .padding

# make sure things are UTF-8...
for i in ChangeLog NEWS ; do
    iconv --from=ISO-8859-1 --to=UTF-8 $i > new
    mv new $i
done

%build
%configure --disable-static --enable-shared

make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -name '*.la' -exec rm -f {} \; 

# clean things up a bit for packaging
( cd example && make clean )
rm -rf example/simple/.deps 
find example/ -type f '(' -name '*.am' -o -name '*.in' ')' -exec rm -v {} \;

%check
(cd tests && make check)

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
#%doc AUTHORS ChangeLog COPYING README NEWS
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc

%files docs
%defattr(-,root,root,-)
%doc COPYING example/
%{_mandir}/man?/*

%files devel
%defattr(-,root,root,-)
%doc COPYING 
%{_includedir}/*
%{_libdir}/*.so

%changelog
