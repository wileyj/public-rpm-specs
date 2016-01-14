Name:           ant
%define         realname apache-ant
Summary:        software project management tool
Version:        1.9.4
Release:        1.%{dist}
Url:            http://ant.apache.org
License:        Apache
Vendor: %{vendor}
Packager: %{packager}
Group:          Application/Web
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:        apache-ant-%{version}.tar.gz
Source1:        ant_path.sh

%description
Apache Ant is a Java-based build tool. In theory, it is kind of like make, without make's wrinkles

%prep
%setup -q -n apache-%{name}-%{version}
%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/etc/profile.d
cp -R %{SOURCE1} %{buildroot}/etc/profile.d/ant_path.sh
cp -R opt %{buildroot}/

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,www)
/opt/apache-ant
/etc/profile.d/ant_path.sh
