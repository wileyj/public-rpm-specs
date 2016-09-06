%if 0%{?amzn} >= 1
%define python python27
BuildRequires: %{python} %{python}-rpm-macros %{python}-devel
Requires: %{python} %{python}-setuptools
%else
%define python python
BuildRequires: %{python} %{python}-rpm-macros %{python}-devel
Requires: %{python} %{python}-setuptools
%endif

BuildRequires: git 

Summary: Tool to allow building RPM packages in chroots
Name: mock
Version: 1.1.9
Release: 1.%{dist}
License: GPLv2+
Vendor: %{vendor}
Packager: %{packager}
Group: Development/Tools
URL: http://fedoraproject.org/wiki/Projects/Mock

Source: https://fedorahosted.org/mock/attachment/wiki/MockTarballs/mock-%{version}.tar.gz
Patch0: mock-1.1.8-mknod.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch
Requires: %{python}-ctypes
Requires: %{python}-decoratortools
Requires: %{python}-hashlib

Requires: createrepo
Requires: pigz
Requires: shadow-utils
Requires: tar
Requires: usermode
Requires: yum >= 2.4

%description
Mock takes an SRPM and builds it in a chroot

%prep
%setup
%patch0

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%{__install} -d -m0755 %{buildroot}%{_localstatedir}/cache/mock/
%{__install} -d -m0755 %{buildroot}%{_localstatedir}/lib/mock/

%{__ln_s} -f consolehelper %{buildroot}%{_bindir}/mock

%{?el5: %{__ln_s} -f centos-5-%{_arch}.cfg %{buildroot}%{_sysconfdir}/mock/default.cfg}
%{?el4: %{__ln_s} -f centos-4-%{_arch}.cfg %{buildroot}%{_sysconfdir}/mock/default.cfg}
%{?el3: %{__ln_s} -f centos-3-%{_arch}.cfg %{buildroot}%{_sysconfdir}/mock/default.cfg}
%{?el2: %{__ln_s} -f centos-2-%{_arch}.cfg %{buildroot}%{_sysconfdir}/mock/default.cfg}

%{?rh9: %{__ln_s} -f redhat-9-%{_arch}.cfg %{buildroot}%{_sysconfdir}/mock/default.cfg}
%{?rh7: %{__ln_s} -f redhat-7-%{_arch}.cfg %{buildroot}%{_sysconfdir}/mock/default.cfg}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%pre
if [ $1 -eq 1 ]; then
    groupadd -r mock &>/dev/null || :
fi

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING INSTALL docs/*.txt
%doc %{_mandir}/man1/mock.1*
%config(noreplace) %{_sysconfdir}/mock/
%config(noreplace) %{_sysconfdir}/pam.d/mock
%config(noreplace) %{_sysconfdir}/security/console.apps/mock
%config %{_sysconfdir}/bash_completion.d/mock.bash
%{_bindir}/mock
%{python_sitelib}/mock/

%defattr(0755, root, root, 0755)
%{_sbindir}/mock

%defattr(0755, root, mock, 02775)
%dir %{_localstatedir}/cache/mock/
%dir %{_localstatedir}/lib/mock/

%changelog
