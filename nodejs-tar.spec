%define nodejs_libdir /usr/lib/node_modules

Name:       nodejs-tar
Version:    0.1.13
Release:    3.%{dist}
Summary:    tar for node
License:    MIT
Vendor: %{vendor}
Packager: %{packager}
Group:      System Environment/Libraries
URL:        https://github.com/isaacs/tar
Source0:    http://registry.npmjs.org/tar/-/tar-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel


Requires:       nodejs
Requires:       nodejs-inherits nodejs-block-stream nodejs-fstream


%description
tar for node

%prep
%setup -q -n package

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}/tar
cp -pr lib tar.js package.json %{buildroot}%{nodejs_libdir}/tar

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{nodejs_libdir}/tar
%doc README.md examples

%changelog
