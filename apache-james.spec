Name:		apache-james
Summary:	apache-james email server
Version:	2.3.2
Release:	1.%{dist}
License:	Apache
Vendor: %{vendor}
Packager: %{packager}
Group:          Application/Web
BuildRoot: 	%{_tmppath}/%{real_name}-%{version}-%{release}-%(%{__id_u} -n)
Source0:	%{name}-%{version}.tar.gz
Source1:	java_home.sh
Requires:	jdk

%define real_name james
%define james_root /opt/%{real_name}-%{version}

%description
The Apache James Project delivers a rich set of open source modules and libraries, written in Java, related to Internet mail communication which build into an advanced enterprise mail server.

%prep 
%setup -q  -n %{real_name}-%{version}
%build 
rm -rf %{buildroot}
mkdir -p %{buildroot}/etc/profile.d
install -m 0755 %{SOURCE1} %{buildroot}/etc/profile.d/
mkdir -p %{buildroot}/opt/%{real_name}-%{version}
pwd
cp -R * %{buildroot}/opt/%{real_name}-%{version}/


%post
ln -sf %{james_root} /opt/james
source /etc/profile.d/java_home.sh
if [ ! -d %{james_root}/apps ]
then
  mkdir %{james_root}/apps
fi
echo "Turning off other mail services..."
if [ -f /etc/init.d/sendmail ]
then
  /etc/init.d/sendmail stop >/dev/null 2>&1 
  echo "Sendmail:           [OFF]"
  /sbin/chkconfig --list | grep sendmail >/dev/null 2>&1
  RETURN1=$?
  if [ $RETURN1 -eq " 0 "]
  then
    /sbin/chkconfig sendmail off >/dev/null 2>&1
    echo "Sendmail chkconfig: [OFF]"
  fi
fi
if [ -f /etc/init.d/postfix ]
then
  /etc/init.d/postfix stop >/dev/null 2>&1
  echo "Postfix:            [OFF]"
  /sbin/chkconfig --list | grep postfix >/dev/null 2>&1
  RETURN2=$?
  if [ $RETURN2 -eq " 0 " ]
  then 
    /sbin/chkconfig postfix off >/dev/null 2>&1
    echo "Postfix chkconfig:  [OFF]"
  fi
fi
echo ""
echo "Puppet will provide james' init script"
echo "Puppet will also chkconfig james to on"

%preun
if [ -f /etc/init.d/james ]
then
  /etc/init.d/james stop
fi
%postun
rm /etc/init.d/james
rm -rf %{james_root}
rm /opt/james
%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%files
%defattr(-,root,root)
%{james_root}
/etc/profile.d/java_home.sh
