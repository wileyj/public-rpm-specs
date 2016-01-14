%define real_name hadoop
%define jdk_version 1.6.0_21
Name:          apache-hadoop
Version:       0.20.2
Release:       1.%{dist}
Summary:       Hadoop Distributed File System and MapReduce implementation
Group:         System Environment/Daemons
URL:           http://hadoop.apache.org/core
Vendor: %{vendor}
Packager: %{packager}
License:       ASL 2.0
BuildArch:     noarch
Source:        %{real_name}-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{real_name}-%{version}-%{release}-root-%(%{__id} -un)
Requires(pre): shadow-utils
AutoReq: 0
Provides: apache-hadoop
AutoProv: 0
Requires:      jdk

# Getting:
# mkdir -p ~/rpmbuild/SOURCES
# cd ~/rpmbuild/SOURCES
# wget http://linorg.usp.br/apache/hadoop/core/hadoop-0.20.0/hadoop-0.20.0.tar.gz

# Recommended Topdir

# So the build does not fail due to unpackaged files or missing doc files:
%define _unpackaged_files_terminate_build 1
%define _missing_doc_files_terminate_build 0
# No debug package:


%description
Apache Hadoop Core is a software platform that lets one easily write and run
applications that process vast amounts of data.

Here's what makes Hadoop especially useful:
 * Scalable: Hadoop can reliably store and process petabytes.
 * Economical: It distributes the data and processing across clusters of
   commonly available computers. These clusters can number into the
   thousands of nodes.
 * Efficient: By distributing the data, Hadoop can process it in parallel on
   the nodes where the data is located. This makes it extremely rapid.
 * Reliable: Hadoop automatically maintains multiple copies of data and
   automatically redeploys computing tasks based on failures.

Hadoop implements MapReduce, using the Hadoop Distributed File System (HDFS).
MapReduce divides applications into many small blocks of work. HDFS creates
multiple replicas of data blocks for reliability, placing them on compute
nodes around the cluster. MapReduce can then process the data where it is
located.

%prep
%setup -n %{real_name}-%{version}

%build
# hadoop-env.sh defaults
%{__sed} -i -e 's|.*JAVA_HOME=.*|export JAVA_HOME=/usr/java/jdk%{jdk_version}|' \
         -e 's|.*HADOOP_CLASSPATH=.*|export HADOOP_CLASSPATH=$HADOOP_CONF_DIR|' \
         -e 's|.*HADOOP_LOG_DIR=.*|export HADOOP_LOG_DIR=/opt/hadoop/log|' \
         -e 's|.*HADOOP_PID_DIR=.*|export HADOOP_PID_DIR=/opt/hadoop/run|' \
         conf/hadoop-env.sh

%install
%{__rm} -rf %{buildroot}
%{__install} -m 0755 -d %{buildroot}/opt/%{real_name}
for D in $(find . -mindepth 1 -maxdepth 1 -type d | cut -c 3- | %{__grep} -Evw 'build|docs|src')
do
  echo "Installing ${D} into /opt/hadoop"
  %{__cp} -a $D %{buildroot}/opt/%{real_name}/
done

echo ROJAS
ls -l *


%{__install} -m 0644 *.jar %{buildroot}/opt/%{real_name}/
%{__install} -m 0644 *.txt %{buildroot}/opt/%{real_name}/
# %{__install} -m 0644 *.xml %{buildroot}/opt/%{real_name}/
%{__install} -m 0755 -d %{buildroot}/opt/hadoop/run
%{__install} -m 0755 -d %{buildroot}/opt/hadoop/log

# Packing list
( cd %{buildroot}
  echo '%defattr(-,root,root,-)'
  echo '%attr(0755,hadoop,hadoop) /opt/hadoop/run'
  echo '%attr(0755,hadoop,hadoop) /opt/hadoop/log'
  find %{buildroot}/opt/%{real_name} -type d -printf '%%%dir %p\n' | %{__sed} -e 's|%{buildroot}||g'
  find %{buildroot}/opt/%{real_name} -type f -printf '%p\n' | %{__grep} -v 'conf/' | %{__sed} -e 's|%{buildroot}||g'
  find %{buildroot}/opt/%{real_name}/conf -type f -printf '%%%config(noreplace) %p\n' | %{__sed} -e 's|%{buildroot}||g'
) > filelist
  find %{buildroot}/opt/%{real_name} -type d -printf '%%%dir %p\n' | %{__sed} -e 's|%{buildroot}||g'


%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%pre
getent group hadoop >/dev/null || \
  lgroupadd -r hadoop
getent passwd hadoop >/dev/null || \
  luseradd -M -r -g hadoop -c 'HDFS runtime user' -s /bin/bash hadoop -d /opt/hadoop/home
exit 0

%check

%post

%preun

%files 
%defattr(-,root,root,-)
%attr(0755,hadoop,hadoop) /opt/hadoop/run
%attr(0755,hadoop,hadoop) /opt/hadoop/log
%config(noreplace) /opt/hadoop/conf/*
/opt/hadoop

%changelog
