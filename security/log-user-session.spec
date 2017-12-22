%define git_repo https://github.com/open-ch/log-user-session
%define git_version %(echo `curl -s  %{git_repo}/releases | grep 'class="css-truncate-target"' | head -1 |  tr -d '\\-</span class="css-truncate-target">'`)
%global git_revision %(echo `git ls-remote %{git_repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define git_summary        %(echo `curl -s %{git_repo} | grep "<title>" | cut -f2 -d ":" | sed 's|</title>||'`)
%define rel_version 1

Name:           log-user-session
Version:        %{git_version}
Release:        %{rel_version}.%{dist}
Summary:        %{git_summary}
Group:          System Environment
License:        MIT
Vendor:         %{vendor}
Packager:       %{packager}
URL:            https://github.com/open-ch/log-user-session
Source1:        %{name}.conf

%description
log-user-session is a program to store the content of a shell session (e.g via
ssh) e.g. for auditing purposes. The tool is intended to be started by the ssh
server daemon. The log is tamper-proof for non-root users.


%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{git_repo} %{name}-%{version}
cd %{name}-%{version}

%build
cd %{name}-%{version}
./autogen.sh
%configure \
        --includedir=%{_includedir}/apr-%{aprver} \
        --with-installbuilddir=%{_libdir}/apr-%{aprver}/build \
        --with-devrandom=/dev/urandom
make %{?_smp_mflags}

%install
cd %{name}-%{version}
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
echo "%{buildroot}%{_bindir}/%{name}
read ans
chown root:root %{buildroot}%{_bindir}/%{name}
chmod u+s %{buildroot}%{_bindir}/%{name}
mkdir -p %{buildroot}%{_sysconfdir}
%__install -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}.conf

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_sysconfdir}/%{name}.conf
%{_mandir}/man8/%{name}.8.gz

