%define name tomcat
%define version 9.0.0
%define install_dir /opt
%define tomcat_user tomcat
%define tomcat_uid 480
%define tomcat_gid 480
%define mysql_connector_version 5.0.8

Summary:   	Apache Tomcat Java JSP/Servlets Server 
Name:      	%{name}
Version:   	%{version} 
Release:   	1.%{dist}
License:   	Apache License Version 2.0 
Packager: 	%{packager}
Vendor: 	%{vendor}
Group:     	Applications/System
Buildroot: 	%{_tmppath}/%{name}-%{version}-root



Source0:   tomcat.tar.gz
Source1:   mysql-connector-java-%{mysql_connector_version}.tar.gz
Source2:   commons-logging-1.1.jar
Source3:   log4j-1.2.13.jar
Source4:   msbase.jar
Source5:   mssqlserver.jar
Source6:   msutil.jar
Source7:   sqljdbc.2008.jar
Source8:   tomcat.init
Source9:   tomcat.include
Source10:  tomcat-juli.jar
Source11:  tomcat-juli-adapters.jar
Source12:  catalina-ws.jar
Source13:  catalina-jmx-remote.jar


BuildRequires: diffutils, perl
Requires: jdk 

%description
Apache Tomcat is the servlet container that is used in the official Reference Implementation for the Java Servlet and JavaServer Pages technologies. The Java Servlet and JavaServer Pages specifications are developed by Sun under the Java Community Process. Apache Tomcat powers numerous large-scale, mission-critical web applications across a diverse range of industries and organizations. 

%package compat 
Summary: Tomcat JDK 1.4 Compatibility Package 
Group: Application/System
Requires: tomcat = %{version} 
%description compat
Tomcat JDK 1.4 Compatibility Package
 
%package mysql
Summary: Tomcat MySQL Java Connector Library 
Group: Application/System
Requires: tomcat = %{version} 
%description mysql
Tomcat MySQL Java Connector Library

%prep
%setup -T -n %{name} -c %{name}
tar -xzf %{SOURCE0}
tar -xzf %{SOURCE1}

%install
%{__rm} -rf %{buildroot}
mkdir -p %{buildroot}%{install_dir}/%{name}-%{version}
mkdir -p %{buildroot}/var/run/%{name}
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{install_dir}/%{name}-%{version}/lib
mkdir -p %{buildroot}%{install_dir}/%{name}-%{version}/temp
mkdir -p %{buildroot}%{install_dir}/%{name}-%{version}/instances
mkdir -p %{buildroot}%{install_dir}/%{name}-%{version}/server
mkdir -p %{buildroot}%{install_dir}/%{name}-%{version}/server/classes
mkdir -p %{buildroot}%{install_dir}/%{name}-%{version}/server/lib
mkdir -p %{buildroot}/u/logs/%{name}
cp -a $RPM_BUILD_DIR/%{name}/* %{buildroot}%{install_dir}/%{name}-%{version}
mv %{buildroot}%{install_dir}/%{name}-%{version}/tomcat/* %{buildroot}%{install_dir}/%{name}-%{version}/
rm -rf %{buildroot}%{install_dir}/%{name}-%{version}/tomcat
rm -rf %{buildroot}%{install_dir}/%{name}-%{version}/test

%{__install} -m0755 mysql-connector-java-%{mysql_connector_version}/mysql-connector-java-%{mysql_connector_version}-bin.jar %{buildroot}%{install_dir}/%{name}-%{version}/lib
%{__install} -m0755 %{SOURCE2} %{buildroot}%{install_dir}/%{name}-%{version}/lib
%{__install} -m0755 %{SOURCE3} %{buildroot}%{install_dir}/%{name}-%{version}/lib
%{__install} -m0755 %{SOURCE4} %{buildroot}%{install_dir}/%{name}-%{version}/lib
%{__install} -m0755 %{SOURCE5} %{buildroot}%{install_dir}/%{name}-%{version}/lib
%{__install} -m0755 %{SOURCE6} %{buildroot}%{install_dir}/%{name}-%{version}/lib
%{__install} -m0755 %{SOURCE7} %{buildroot}%{install_dir}/%{name}-%{version}/lib/sqljdbc.jar
%{__install} -m0755 %{SOURCE10} %{buildroot}%{install_dir}/%{name}-%{version}/lib
%{__install} -m0755 %{SOURCE11} %{buildroot}%{install_dir}/%{name}-%{version}/lib
%{__install} -m0755 %{SOURCE12} %{buildroot}%{install_dir}/%{name}-%{version}/lib
%{__install} -m0755 %{SOURCE13} %{buildroot}%{install_dir}/%{name}-%{version}/lib
#%{__install} -m0755 $RPM_BUILD_DIR/%{name}/mysql-connector-java-%{mysql_connector_version}/mysql-connector-java-%{mysql_connector_version}-bin.jar %{buildroot}%{install_dir}/%{name}-%{version}/lib

%{__install} -m0755 %{SOURCE8} %{buildroot}%{_initrddir}/%{name}
%{__install} -m0755 %{SOURCE9} %{buildroot}%{_initrddir}/
chmod +x %{buildroot}%{install_dir}/%{name}-%{version}/bin/catalina.sh
chmod +x %{buildroot}%{install_dir}/%{name}-%{version}/bin/setclasspath.sh


DIR=`pwd`
cd %{buildroot}%{install_dir}
%__ln_s -f  /opt/%{name}-%{version}  %{name}
%__ln_s -f  /opt/%{name}-%{version}/webapps  %{name}-%{version}/server
cd %{name}-%{version}
%__rm -rf logs
%__ln_s -f /u/logs/%{name} logs
cd $DIR

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%pre
# Add the "tomcat" user
getent group %{tomcat_group} >/dev/null || groupadd -r %{tomcat_group}
getent passwd %{tomcat_user} >/dev/null || \
    useradd -r -g %{tomcat_group} -s /sbin/nologin \
    -d %{tomcat_home} -c "tomcat user"  %{tomcat_user}
exit 0


%post
/bin/chown -R %{tomcat_user}:%{tomcat_group} %{install_dir}/%{name}-%{version}
/bin/chmod -R g+r %{install_dir}/%{name}-%{version}
/bin/chown -R %{tomcat_user}:%{tomcat_group} /var/run/%{name}
/sbin/chkconfig --add tomcat


# Secure the shutdown port
perl -pi -e '$rand = crypt(rand(999), "rF"); s|shutdown=\"SHUTDOWN\"|shutdown=\"$rand\"|' %{install_dir}/%{name}-%{version}/conf/server.xml

# Setup a user for /manager
rand=`echo "${RANDOM}aE3bJjV3AbBngAcdEFgHaQNRdaa" | sort | awk -F "" {' print $1$2$14$5$10$2$19$7 '}`
mv %{install_dir}/%{name}-%{version}/conf/tomcat-users.xml %{install_dir}/%{name}-%{version}/conf/tomcat-users.xml.orig
cat > %{install_dir}/%{name}-%{version}/conf/tomcat-users.xml <<EOF
<tomcat-users>
  <user name="tomcat" password="tomcat" roles="tomcat" />
  <user name="role1"  password="tomcat" roles="role1"  />
  <user name="both"   password="tomcat" roles="tomcat,role1" />
  <user name="admin"  password="$rand" roles="manager,tomcat,role1" />
</tomcat-users>
EOF

%preun
if [ -e /var/run/%{name}/%{name}-%{version}.pid ]; then
	%{_initrddir}/%{name} stop
fi
/sbin/chkconfig --del tomcat

%postun

%files 
%defattr(-, tomcat,tomcat)
%{install_dir}/%{name}-%{version}/LICENSE
%{install_dir}/%{name}-%{version}/NOTICE
%{install_dir}/%{name}-%{version}/RELEASE-NOTES
%{install_dir}/%{name}-%{version}/RUNNING.txt
%{install_dir}/%{name}-%{version}/bin
%{install_dir}/%{name}-%{version}/temp
%{install_dir}/%{name}-%{version}/logs
%{install_dir}/%{name}-%{version}/instances
%{install_dir}/%{name}-%{version}/lib
%{install_dir}/%{name}-%{version}/server
%{install_dir}/%{name}-%{version}/webapps
%{install_dir}/%{name}
/u/logs/%{name}
%{_initrddir}/%{name}
%{_initrddir}/%{name}.include
%config  %{install_dir}/%{name}-%{version}/conf
%config(noreplace) %{install_dir}/%{name}-%{version}/conf/server.xml 
%{install_dir}/%{name}-%{version}/res*
%{install_dir}/%{name}-%{version}/modules/jdbc-pool*
%{install_dir}/%{name}-%{version}/java*
%{install_dir}/%{name}-%{version}/BUILDING.txt
%{install_dir}/%{name}-%{version}/KEYS
%{install_dir}/%{name}-%{version}/SVN-MERGE.txt
%{install_dir}/%{name}-%{version}/TOMCAT-NEXT.txt
%{install_dir}/%{name}-%{version}/build.properties.default
%{install_dir}/%{name}-%{version}/build.xml

%files mysql 
%{install_dir}/%{name}-%{version}/lib/mysql-connector-java-%{mysql_connector_version}-bin.jar  
%{install_dir}/%{name}-%{version}/mysql-connector-java*


%changelog
