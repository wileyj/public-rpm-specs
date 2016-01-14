Name:           sumologic-conf
Summary:        sumologic-conf
Version:        1.0.0
Release:	1.%{dist}
License:        Restricted
Vendor: 	%{vendor}
Packager: 	%{packager}
Group:          Development/Libraries
Provides:	%{name}

%description
%{summary}

%prep
%setup -q -c -T
%build
%install
%__mkdir_p %{buildroot}%{_sysconfdir}
%__mkdir_p %{buildroot}%{_sysconfdir}/sumo.d

cat <<EOF> %{buildroot}%{_sysconfdir}/sumo.conf
accessid=<access id>
accesskey=<access key>
syncSources=/etc/sumo.d/
EOF

%post
%__sed -i "1s/^/name=`/bin/hostname`\n/" /etc/sumo.conf

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root)
%attr(644, root, root) %{_sysconfdir}/sumo.conf
%dir %{_sysconfdir}/sumo.d
