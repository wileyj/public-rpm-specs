Name:       automake
Version:    1.15
Release:    1.%{dist}
Summary:    Automatically generate Makefiles
Group:      Development/Tools
License:    GNU GPL
URL:        http://www.gnu.org/software/automake/
Vendor: %{vendor}
Packager: %{packager}
Source0:    http://ftp.gnu.org/gnu/automake/%{name}-%{version}.tar.xz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch
BuildRequires:  autoconf 
Requires:   autoconf
Requires(post):  info
Requires(preun): info
AutoReq: no

%description
Automake is a tool for automatically generating Makefiles compliant with the 
GNU Coding Standards.

%prep
%setup -q

%build
%configure --prefix=/usr --docdir=/usr/share/doc/automake-1.11
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_infodir}/dir

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%post
/sbin/install-info %{_infodir}/automake.info.gz %{_infodir}/dir || :

%preun
if [ $1 = 0 ]; then
/sbin/install-info --delete %{_infodir}/automake.info.gz %{_infodir}/dir || :
fi 

%files
%defattr(-,root,root,-)
%doc AUTHORS README THANKS NEWS
%{_bindir}/*
%{_infodir}/*.info*
%{_datadir}/automake-%{version}
%{_datadir}/aclocal-%{version}
%{_datadir}/aclocal/README
%{_mandir}/man1/*
%{_docdir}/*/*

%changelog
