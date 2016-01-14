%define nodejs_libdir /usr/lib/node_modules

Name:       nodejs-archy
Version:    0.0.2
Release:    3.%{dist}
Summary:    Renders nested hierarchies with unicode pipes
License:    MIT
Vendor: %{vendor}
Packager: %{packager}
Group:      System Environment/Libraries
URL:        https://github.com/substack/archy
Source0:    http://registry.npmjs.org/archy/-/archy-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel
Requires:       nodejs

%description
Render nested hierarchies with unicode pipes, `npm ls` style.

%prep
%setup -q -n package

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}/archy
cp -p index.js package.json %{buildroot}%{nodejs_libdir}/archy

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{nodejs_libdir}/archy
%doc README.markdown examples

%changelog
