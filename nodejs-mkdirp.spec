%define nodejs_libdir /usr/lib/node_modules

Name:       nodejs-mkdirp
Version:    0.3.1
Release:    3.%{dist}
Summary:    Recursively mkdir, like `mkdir -p`
License:    MIT
Vendor: %{vendor}
Packager: %{packager}
Group:      Development/Libraries
URL:        https://github.com/substack/node-mkdirp
Source0:    http://registry.npmjs.org/mkdirp/-/mkdirp-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel
Requires:       nodejs

%description
mkdirp

%prep
%setup -q -n package

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}/mkdirp
cp -pr index.js package.json %{buildroot}%{nodejs_libdir}/mkdirp

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{nodejs_libdir}/mkdirp
%doc README.markdown examples

%changelog
