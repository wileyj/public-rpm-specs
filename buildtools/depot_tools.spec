%define repo https://chromium.googlesource.com/chromium/tools/depot_tools.git
%define gitversion %(echo `date +%s`)
%define pathname /opt/depot_tools
%define depot_tools_user depot_tools
%define depot_tools_group depot_tools
%define uid 1501
%define gid 1501

Name:           depot_tools
Summary:        depot_tools
Version:        %{gitversion}
Release:	1.%{dist}
Url:            https://chromium.googlesource.com/chromium/tools/depot_tools.git
License:        GPL
Vendor: 	%{vendor}
Packager: 	%{packager}
Group:          Development/Applications
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
Provides:	depot_tools

%description
Google depot_tools

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
git submodule init
git submodule update

%build
cd %{name}-%{version}

%install
cd %{name}-%{version}
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pathname}
cp -R * %{buildroot}%{pathname}/
mkdir -p %{buildroot}%{_sysconfdir}/profile.d

cat <<EOF> %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh
export PATH=%{pathname}:$PATH
EOF

%pre
getent group %{depot_tools_group} >/dev/null || /usr/sbin/groupadd %{depot_tools_group} -g %{gid} 2>/dev/null
getent passwd %{depot_tools_user} >/dev/null || /usr/sbin/useradd -u %{uid} -c '%{depot_tools_user}' -g %{gid} -d %{pathname} -s /bin/bash %{depot_tools_user} 2>/dev/null
exit 0


%post
chown -R %{depot_tools_user}:%{depot_tools_group} %{pathname}
export PATH=$PATH:%{pathname}
cd %{pathname}
%{pathname}/gclient config https://chromium.googlesource.com/chromium/tools/depot_tools.git
%{pathname}/gclient sync
chown -R %{depot_tools_user}:%{depot_tools_group} %{pathname}
exit 0

%postun
/usr/sbin/userdel %{depot_tools_user}
/usr/sbin/groupdel %{depot_tools_group}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,%{depot_tools_user},%{depot_tools_group})
%dir %{pathname}
%{pathname}/*
%attr(755, root, root) %{_sysconfdir}/profile.d/%{name}.sh


