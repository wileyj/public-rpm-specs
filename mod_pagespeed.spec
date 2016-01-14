%define major 1
Name: mod_pagespeed
Version: %{major}.0
Release: 1.%{dist}
License: Apache
Vendor: %{vendor}
Packager: %{packager}
Summary: Build of mod_pagespeed
Group: Applications/Internet
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Source0: mod_pagespeed-x86_64.so
Source1: pagespeed.conf
BuildRequires: httpd
Requires: httpd
Provides: mod_pagespeed = 0:%{version}-%{release}
AutoReq: 0

%define opt_apache /opt/apache2.2

%description
mod_pagespeed

%prep


%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{opt_apache}/modules
mkdir -p $RPM_BUILD_ROOT%{opt_apache}/mod_pagespeed/{files,cache}
mkdir -p $RPM_BUILD_ROOT%{opt_apache}/conf/default
cp %{SOURCE0} $RPM_BUILD_ROOT%{opt_apache}/modules/mod_pagespeed.so
cp %{SOURCE1} $RPM_BUILD_ROOT%{opt_apache}/conf/default/pagespeed.conf

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-, root, root)
%{opt_apache}/modules/mod_pagespeed.so
%{opt_apache}/conf/default/pagespeed.conf
%attr(-,apache,www) %{opt_apache}/mod_pagespeed
%attr(-,apache,www) %{opt_apache}/mod_pagespeed/files
%attr(-,apache,www) %{opt_apache}/mod_pagespeed/cache


%changelog
