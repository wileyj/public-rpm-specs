Summary: Interactive process viewer
Name: htop
Version: 0.9
Release: 1.%{dist}
License: GPL
Vendor: %{vendor}
Packager: %{packager}
Group: Applications/System
URL: http://htop.sourceforge.net/
Source: http://dl.sf.net/htop/htop-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gcc >= 3.0, ncurses-devel

%description
htop is an interactive process viewer for Linux.

%prep
%setup

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README
%doc %{_mandir}/man1/htop.1*
%{_bindir}/htop
%{_datadir}/applications/htop.desktop
%{_datadir}/pixmaps/htop.png

%changelog
