%define nodejs_libdir /usr/lib/node_modules

%global git_hash e1f8f25

Name:       nodejs-proto-list
Version:    1.0.0
Release:    3.%{dist}
Summary:    A list of objects bound by prototype chain
License:    MIT
Vendor: %{vendor}
Packager: %{packager}
Group:      System Environment/Libraries
URL:        https://github.com/isaacs/proto-list
# download from https://github.com/isaacs/proto-list/tarball/%%{version}
Source0:    isaacs-proto-list-%{version}-0-g%{git_hash}.tar.gz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel
Requires:       nodejs

#BuildRequires:  nodejs-tap

%description
A list of objects bound by prototype chain.  Used for the Node.js package
manager (npm) configuration.

%prep
%setup -q -n isaacs-proto-list-7311c7f

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_libdir}
cp -p proto-list.js %{buildroot}%{nodejs_libdir}

# We currently don't run tests because I'd have to file another ten or
# so review reuqests for the node.js TAP testing framework and methinks there
# are enough of those for now.  ;-)
##%%check
##%%nodejs proto-list.js

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%{nodejs_libdir}/proto-list.js
%doc LICENSE README.md

%changelog
