# https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon-3.2.0.tgz
# https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-3.2.0.tgz

#%define lver amazon
%define lver rhel70
%define app_dir /opt/%{name}/product/%{version}

Summary: Mongo DB Binary Builds
Name: mongodb
Version: 3.2.0
Release: 1.%{dist}
License: GPL
Vendor: %{vendor}
Packager: %{packager}
Group: Applications/System
URL: http://mongodb.org
Requires: libpcap
Source: http://fastdl.mongodb.org/linux/mongodb-linux-x86_64-%{lver}-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: x86_64
Requires: mongodb-client
AutoReq: 0

%description
Mongo (from "huMONGOus") is a schema-free document-oriented database.
It features dynamic profileable queries, full indexing, replication
and fail-over support, efficient storage of large binary data objects,
and auto-sharding.

%package client
Group: Applications/System
Summary: Mongo DB Binary client build

%description client
Mongo (from "huMONGOus") is a schema-free document-oriented database.
It features dynamic profileable queries, full indexing, replication
and fail-over support, efficient storage of large binary data objects,
and auto-sharding. This package is the client ONLY.

%prep
%setup -n %{name}-linux-x86_64-%{lver}-%{version}

%postun  -n mongodb-client
if [ -f %{app_dir} ]
then
  %__rm -rf %{app_dir}
fi

%install
%{__rm} -rf %{buildroot}
mkdir -p %{buildroot}%{app_dir}
%{__install} -m0755 bin/* %{buildroot}/%{app_dir}

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files client
%defattr(-, mongodb, mongodb, 0755)
%dir %{app_dir}
%{app_dir}/mongo
%{app_dir}/mongodump
%{app_dir}/bsondump
%{app_dir}/mongoexport
%{app_dir}/mongostat
%{app_dir}/mongotop

%files
%defattr(-, mongodb, mongodb, 0755)
%{app_dir}/mongod
%{app_dir}/mongofiles
%{app_dir}/mongoimport
%{app_dir}/mongoperf
%{app_dir}/mongorestore
%{app_dir}/mongos
%{app_dir}/mongostat
%{app_dir}/mongooplog

%changelog
* Tue Jun 16 2015 Jesse Wiley <jesse@risingtidegames.com> 3.0.4-1
- creating for Chris Price
