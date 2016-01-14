%define nodejs_libdir /usr/lib/node_modules

Name:       nodejs-node-uuid
Version:    1.3.3
Release:    3.%{dist}
Summary:    RFC4122v4 UUID generator for Node.js
License:    MIT or GPL+
Vendor: %{vendor}
Packager: %{packager}
Group:      Development/Libraries
URL:        https://github.com/isaacs/node-semver
Source0:    http://registry.npmjs.org/node-uuid/-/node-uuid-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel
Requires:       nodejs

Obsoletes:      nodejs-uuid < 1.2.0-2
Provides:       nodejs-uuid = %{version}-%{release}

%description
Simple, fast generation of RFC4122v4 and non-RFC compact UUIDs.  It runs in
node.js and many browsers.

%prep
%setup -q -n package

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}/node-uuid
cp -p uuid.js package.json %{buildroot}%{nodejs_libdir}/node-uuid

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{nodejs_libdir}/node-uuid
%doc README.md LICENSE.md

%changelog
