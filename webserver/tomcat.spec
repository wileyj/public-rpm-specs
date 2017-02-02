%define repo https://github.com/apache/tomcat
%define gitversion %(echo `curl -s %{repo}/releases | grep 'class="tag-name"' | head -1 |sed 's/TOMCAT.//' | tr '_' '.' |  tr -d '\\-</span class="tag-name">vr'`)
%global revision %(echo `git ls-remote %{repo}.git  | head -1 | cut -f 1| cut -c1-7`)
%define rel_version 1

%define tomcat_prefix /opt/%{name}

%define tomcat_user tomcat
%define tomcat_group tomcat
%define tomcat_uid 480
%define tomcat_gid 480

Summary:   	Apache Tomcat Java JSP/Servlets Server 
Name:      	tomcat
Version:   	%{gitversion} 
Release:   	%{rel_version}.%{revision}.%{dist}
License:   	Apache License Version 2.0 
Packager: 	%{packager}
Vendor: 	%{vendor}
Group:     	Applications/System
Source1:   	tomcat.init
Source2:	tomcat.include

BuildRequires: ant jdk
Requires: jdk 

%description
Apache Tomcat is the servlet container that is used in the official Reference Implementation for the Java Servlet and JavaServer Pages technologies. The Java Servlet and JavaServer Pages specifications are developed by Sun under the Java Community Process. Apache Tomcat powers numerous large-scale, mission-critical web applications across a diverse range of industries and organizations. 

%prep
if [ -d %{name}-%{version} ];then
    rm -rf %{name}-%{version}
fi
git clone %{repo} %{name}-%{version}
cd %{name}-%{version}
source /etc/profile.d/ant.sh

%build
cd %{name}-%{version}
%{_bindir}/ant 

%install
cd %{name}-%{version}
%__mkdir_p %{buildroot}/var/run/%{name}
%__mkdir_p %{buildroot}/var/log/%{name}
%__mkdir_p %{buildroot}%{_initrddir}
%__mkdir_p %{buildroot}%{tomcat_prefix}-%{version}/instances

%__cp -R output/build/lib %{buildroot}%{tomcat_prefix}-%{version}/lib
%__cp -R output/build/conf %{buildroot}%{tomcat_prefix}-%{version}/conf
%__cp -R output/build/bin %{buildroot}%{tomcat_prefix}-%{version}/bin
%__cp -R output/build/temp %{buildroot}%{tomcat_prefix}-%{version}/temp
%__cp -R output/build/webapps %{buildroot}%{tomcat_prefix}-%{version}/webapps

%{__install} -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%{__install} -m0755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}.include
%__ln_s -f  %{tomcat_prefix}-%{version}  %{buildroot}%{tomcat_prefix}
%__ln_s -f  %{tomcat_prefix}-%{version}/webapps  %{buildroot}%{tomcat_prefix}-%{version}/server
%__ln_s -f  /var/log/%{name} %{buildroot}%{tomcat_prefix}-%{version}/logs

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%%{name}-contrib-%{version}" != "/" ] && %__rm -rf %{_builddir}/%%{name}-contrib-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}
[ "%{_builddir}/%{pkgname}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{pkgname}-%{version}


%pre
# Add the "tomcat" user
getent group %{tomcat_group} >/dev/null || groupadd -r %{tomcat_group}
getent passwd %{tomcat_user} >/dev/null || useradd -r -g %{tomcat_group} -s /sbin/nologin -d %{tomcat_prefix} -c "tomcat user"  %{tomcat_user}
exit 0

%post
/bin/chown -R %{tomcat_user}:%{tomcat_group} %{install_dir}/%{name}-%{version}
/bin/chmod -R g+r %{tomcat_prefix}/%{version}
/bin/chown -R %{tomcat_user}:%{tomcat_group} /var/run/%{name}
/sbin/chkconfig --add %{name}


# Secure the shutdown port
perl -pi -e '$rand = crypt(rand(999), "rF"); s|shutdown=\"SHUTDOWN\"|shutdown=\"$rand\"|' %{tomcat_prefix}/%{version}/conf/server.xml

# Setup a user for /manager
rand=`echo "${RANDOM}aE3bJjV3AbBngAcdEFgHaQNRdaa" | sort | awk -F "" {' print $1$2$14$5$10$2$19$7 '}`
cat <<EOF> %{tomcat_prefix}/%{version}/conf/tomcat-users.xml
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
/sbin/chkconfig --del %{name}

%postun

%files 
%defattr(-, %{tomcat_user},%{tomcat_group})
%dir %{tomcat_prefix}-%{version}
%dir %{tomcat_prefix}-%{version}/bin
%dir %{tomcat_prefix}-%{version}/temp
%dir /var/log/%{name}
%dir %{tomcat_prefix}-%{version}/instances
%dir %{tomcat_prefix}-%{version}/lib
%dir %{tomcat_prefix}-%{version}/webapps

%{tomcat_prefix}
%{tomcat_prefix}-%{version}
%{tomcat_prefix}-%{version}/bin/*
%{tomcat_prefix}-%{version}/lib/*
%{tomcat_prefix}-%{version}/webapps/*
%{tomcat_prefix}-%{version}/server
%{_initrddir}/%{name}
%{_initrddir}/%{name}.include
%config  %{tomcat_prefix}-%{version}/conf
%config(noreplace) %{tomcat_prefix}-%{version}/conf/server.xml 

%changelog
