%define name chkrootkit
%define version 0.52
%define release 1
Summary: chkrootkit is a tool to locally check for signs of a rootkit
Name: %name
Version: %version
Release: %release.%{dist}
License: GPL
Vendor: %{vendor}
Packager: %{packager}
Group: Applications/Internet
Url: http://www.chkrootkit.org/
Source: %name.tar.gz
BuildRoot: %_tmppath/%{name}-buildroot
Requires: gcc

%description
%{summary}

%prep
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%setup -q

%build
make OPTS="$RPM_OPT_FLAGS"

%install
rm -rf %{buildroot}
%__mkdir_p $RPM_BUILD_ROOT/%{_bindir}
%__install -m 500 chkdirs $RPM_BUILD_ROOT/%{_bindir}
%__install -m 500 chkrootkit $RPM_BUILD_ROOT/%{_bindir}
%__install -m 500 check_wtmpx $RPM_BUILD_ROOT/%{_bindir}
%__install -m 500 chkproc $RPM_BUILD_ROOT/%{_bindir}
%__install -m 500 chkwtmp $RPM_BUILD_ROOT/%{_bindir}
%__install -m 500 ifpromisc $RPM_BUILD_ROOT/%{_bindir}
%__install -m 500 chklastlog $RPM_BUILD_ROOT/%{_bindir}
%__install -m 500 chkutmp $RPM_BUILD_ROOT/%{_bindir}
%__install -m 500 strings-static $RPM_BUILD_ROOT/%{_bindir}

%clean
#[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT



%files
%{_bindir}/chkdirs
%{_bindir}/chkrootkit
%{_bindir}/check_wtmpx
%{_bindir}/chkproc
%{_bindir}/chkwtmp
%{_bindir}/ifpromisc
%{_bindir}/chklastlog
%{_bindir}/chkutmp
%{_bindir}/strings-static

