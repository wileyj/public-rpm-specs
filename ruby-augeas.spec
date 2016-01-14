%include %{_rpmconfigdir}/macros.d/macros.ruby


Name:           ruby-augeas
Version:        0.5.0
Release:        4.%{dist}
Summary:        Ruby bindings for Augeas
Group:          Development/Languages

License:        LGPLv2+
Packager: %{packager}
Vendor: %{vendor}
URL:            http://augeas.net
Source0:        http://download.augeas.net/ruby/ruby-augeas-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ruby rubygem-rake 
#rubygem-test-unit
BuildRequires:  ruby-devel
BuildRequires:  augeas-devel >= 1.0.0
BuildRequires:  pkgconfig
Requires:       ruby
Requires:       augeas-libs >= 1.0.0
Provides:       ruby-augeas = %{version}

%description
Ruby bindings for augeas.

%prep
%setup -q


%build
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
rake build

%install
rm -rf %{buildroot}
install -d -m0755 %{buildroot}%{ruby_vendorlibdir}
install -d -m0755 %{buildroot}%{ruby_vendorarchdir}
install -p -m0644 lib/augeas.rb %{buildroot}%{ruby_vendorlibdir}
install -p -m0755 ext/augeas/_augeas.so %{buildroot}%{ruby_vendorarchdir}

#%check
#ruby tests/tc_augeas.rb

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root,-)
%doc COPYING README.rdoc NEWS
%{ruby_vendorlibdir}/augeas.rb
%{ruby_vendorarchdir}/_augeas.so


%changelog
