%define nodejs_libdir /usr/lib/node_modules

Name:       nodejs-fstream-ignore
Version:    0.0.5
Release:    3.%{dist}
Summary:    A thing for ignoring files based on globs
License:    MIT
Vendor: %{vendor}
Packager: %{packager}
Group:      System Environment/Libraries
URL:        https://github.com/isaacs/fstream-ignore
Source0:    http://registry.npmjs.org/fstream-ignore/-/fstream-ignore-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel

Requires:       nodejs
Requires:       nodejs-minimatch nodejs-fstream nodejs-inherits

%description
%{summary}.

%prep
%setup -q -n package

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}/fstream-ignore
cp -pr ignore.js package.json %{buildroot}%{nodejs_libdir}/fstream-ignore

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{nodejs_libdir}/fstream-ignore
%doc README.md example

%changelog
