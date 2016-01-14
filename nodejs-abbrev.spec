%define nodejs_libdir /usr/lib/node_modules

Name:       nodejs-abbrev
Version:    1.0.3
Release:    3.%{dist}
Group:      Development/Libraries
Summary:    Abbreviation calculator for Node.js
License:    MIT
Vendor: %{vendor}
Packager: %{packager}
URL:        https://github.com/isaacs/abbrev-js
Source0:    http://registry.npmjs.org/abbrev/-/abbrev-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel
Requires:       nodejs

%description
Calculate the set of unique abbreviations for a given set of strings.

%prep
%setup -q -n package

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}/abbrev
cp -pr lib package.json %{buildroot}%{nodejs_libdir}/abbrev

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{nodejs_libdir}/abbrev
%doc README.md
