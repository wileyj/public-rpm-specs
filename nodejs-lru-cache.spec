%define nodejs_libdir /usr/lib/node_modules

Name:       nodejs-lru-cache
Version:    1.1.0
Release:    3.%{dist}
Summary:    A cache object that deletes the least recently used items
License:    MIT
Vendor: %{vendor}
Packager: %{packager}
Group:      System Environment/Libraries
URL:        https://github.com/isaacs/node-lru-cache
Source0:    http://registry.npmjs.org/lru-cache/-/lru-cache-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel
Requires:       nodejs

%description
lru caching for nodejs

%prep
%setup -q -n package

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}/lru-cache
cp -pr lib package.json %{buildroot}%{nodejs_libdir}/lru-cache

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{nodejs_libdir}/lru-cache
%doc README.md LICENSE

%changelog
