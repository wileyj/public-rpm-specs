Name:           grails
%define         realname grails 
Summary:        java web application framework
Version:        3.0.11
Release:        1.%{dist}
Url:            http://grails.codehaus.org/
License:        Apache
Vendor: %{vendor}
Packager: %{packager}
Group:          Application/Web
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:        %{name}-%{version}.tar.gz
Source1:        grails_path.sh

%description
It's an open-source web application framework that leverages the Groovy language
and complements Java Web development. Grails aims to make development 
as simple as possible

%prep
%setup -q
%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/etc/profile.d
mkdir -p %{buildroot}/opt/%{name}
cp -R %{SOURCE1} %{buildroot}/etc/profile.d/grails_path.sh
pwd
cp -R * %{buildroot}/opt/%{name}

#cp -R /usr/src/redhat/BUILD/%{name}-%{version} %{buildroot}/opt/grails

%postun
rm -rf /opt/%{name}

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,www)
%attr(775,root,www) /opt/%{name}
%attr(755,root,www) /etc/profile.d/grails_path.sh



