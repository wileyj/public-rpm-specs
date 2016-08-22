Name:          puppetdb-terminus
Version:       3
Release:       1.%{?dist}
Summary:       Metapackage to allow easy upgrades from PuppetDB 2

License:       ASL 2.0
URL:           http://docs.puppetlabs.com
Source0:       README
Requires:      puppetdb-termini
BuildArch:     noarch


%description
This is a metapackage to allow easier upgrades from people running PuppetDB 2.
This pulls in puppetdb-termini (needed for PDB3) and not puppetdb-terminus.


%prep
cp %{SOURCE0} .


%build


%install
rm -rf $RPM_BUILD_ROOT


%files
%doc README


%changelog
* Fri Jul 10 2015 Michael Stahnke <stahnma@puppetlabs.com> - 3
- Initial package
