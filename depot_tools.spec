Name:           depot_tools
Summary:        depot_tools
Version:        1.0.0
Release:	1.%{dist}
Url:            https://chromium.googlesource.com/chromium/tools/depot_tools.git
License:        GPL
Vendor: 	%{vendor}
Packager: 	%{packager}
Group:          Development/Applications
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
Source0:	%{name}.tar.gz
Provides:	depot_tools

%description
Google depot_tools

%prep
%setup -n %{name} -T -b 0

%build
git pull

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt/%{name}
cp -R * %{buildroot}/opt/%{name}/
mkdir -p %{buildroot}/etc/profile.d

cat <<EOF> %{buildroot}/etc/profile.d/depot_tools.sh
export PATH=$PATH:/opt/%{name}
EOF

%post
export PATH=$PATH:/opt/%{name}
su - ec2-user -c "export PATH=$PATH:/opt/depot_tools; cd /opt/%{name} && gclient sync"

%postun
rm -rf /opt/%{name}
rm -f /etc/profile.d/depot_tools.sh
 
%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files
%defattr(-,ec2-user,ec2-user)
/opt/%{name}
%attr(755, root, root) /etc/profile.d/depot_tools.sh


