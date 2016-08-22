#   Licensed to the Apache Software Foundation (ASF) under one or more
#   contributor license agreements.  See the NOTICE file distributed with
#   this work for additional information regarding copyright ownership.
#   The ASF licenses this file to You under the Apache License, Version 2.0
#   (the "License"); you may not use this file except in compliance with
#   the License.  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

#
# RPM Spec file for Hadoop version 2.6.2
#

%define name         hadoop
%define version      2.7.2
%define release      1.%{dist}

# Installation Locations
%define _prefix      /opt/hadoop
%define _bin_dir     %{_prefix}/bin
%define _conf_dir    /etc/hadoop
%define _lib_dir     %{_prefix}/lib
%define _lib64_dir   %{_prefix}/lib64
%define _libexec_dir %{_prefix}/libexec
%define _log_dir     /var/log/hadoop
%define _pid_dir     /var/run/hadoop
%define _sbin_dir    %{_prefix}/sbin
%define _share_dir   %{_prefix}/share
%define _var_dir     %{_datadir}

# Build time settings
%define _build_dir  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id} -un)
%define _final_name %{name}-%{version}
%define debug_package %{nil}

# Disable brp-java-repack-jars for aspect J
%define __os_install_post    \
#    /usr/lib/rpm/amazon/brp-compress \
#    %{!?__debug_package:/usr/lib/rpm/amazon/brp-strip %{__strip}} \
#    /usr/lib/rpm/amazon/brp-strip-static-archive %{__strip} \
#    /usr/lib/rpm/amazon/brp-strip-comment-note %{__strip} %{__objdump} \
    /usr/lib/rpm/brp-python-bytecompile %{nil}

%define _use_internal_dependency_generator 0

%global hadoop_arch Linux-amd64-64

Summary: The Apache Hadoop project develops open-source software for reliable, scalable, distributed computing
License: Apache License, Version 2.0
URL: http://hadoop.apache.org/core/
Vendor: Apache Software Foundation
Group: Development/Libraries
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{_final_name}.tar.gz
Prefix: %{_prefix}
Prefix: %{_conf_dir}
Prefix: %{_log_dir}
Prefix: %{_pid_dir}
Buildroot: %{_build_dir}
Requires: sh-utils, textutils, /usr/sbin/useradd, /usr/sbin/usermod, /sbin/chkconfig, /sbin/service, jdk >= 1.6
AutoReqProv: no
Provides: hadoop

%description
The Apache Hadoop project develops open-source software for reliable, scalable, 
distributed computing.  Hadoop includes these subprojects:

Hadoop Common: The common utilities that support the other Hadoop subprojects.

%prep
%setup -n %{name}-%{version}

%build
if [ -d ${RPM_BUILD_DIR}%{_prefix} ]; then
  rm -rf ${RPM_BUILD_DIR}%{_prefix}
fi

if [ -d ${RPM_BUILD_DIR}%{_log_dir} ]; then
  rm -rf ${RPM_BUILD_DIR}%{_log_dir}
fi

if [ -d ${RPM_BUILD_DIR}%{_conf_dir} ]; then
  rm -rf ${RPM_BUILD_DIR}%{_conf_dir}
fi

if [ -d ${RPM_BUILD_DIR}%{_pid_dir} ]; then
  rm -rf ${RPM_BUILD_DIR}%{_pid_dir}
fi

#########################
#### INSTALL SECTION ####
#########################
%install
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}
mkdir -p ${RPM_BUILD_ROOT}%{_bin_dir}
mkdir -p ${RPM_BUILD_ROOT}%{_lib_dir}
mkdir -p ${RPM_BUILD_ROOT}%{_lib64_dir}
mkdir -p ${RPM_BUILD_ROOT}%{_libexec_dir}
mkdir -p ${RPM_BUILD_ROOT}%{_log_dir}
mkdir -p ${RPM_BUILD_ROOT}%{_conf_dir}
mkdir -p ${RPM_BUILD_ROOT}%{_pid_dir}
mkdir -p ${RPM_BUILD_ROOT}%{_sbin_dir}
mkdir -p ${RPM_BUILD_ROOT}%{_share_dir}
mkdir -p ${RPM_BUILD_ROOT}%{_var_dir}

mv ${RPM_BUILD_DIR}/%{_final_name}/bin/* ${RPM_BUILD_ROOT}%{_bin_dir}
mv ${RPM_BUILD_DIR}/%{_final_name}/etc/hadoop/* ${RPM_BUILD_ROOT}%{_conf_dir}
mv ${RPM_BUILD_DIR}/%{_final_name}/lib/* ${RPM_BUILD_ROOT}%{_lib_dir}
mv ${RPM_BUILD_DIR}/%{_final_name}/libexec/* ${RPM_BUILD_ROOT}%{_libexec_dir}
mv ${RPM_BUILD_DIR}/%{_final_name}/sbin/* ${RPM_BUILD_ROOT}%{_sbin_dir}
mv ${RPM_BUILD_DIR}/%{_final_name}/share/* ${RPM_BUILD_ROOT}%{_share_dir}
rm -rf ${RPM_BUILD_DIR}/%{_final_name}/etc

%pre
getent group hadoop 2>/dev/null >/dev/null || /usr/sbin/groupadd -r hadoop

%post
bash ${RPM_INSTALL_PREFIX0}/sbin/update-hadoop-env.sh \
       --prefix=${RPM_INSTALL_PREFIX0} \
       --bin-dir=${RPM_INSTALL_PREFIX0}/bin \
       --sbin-dir=${RPM_INSTALL_PREFIX0}/sbin \
       --conf-dir=${RPM_INSTALL_PREFIX1} \
       --log-dir=${RPM_INSTALL_PREFIX2} \
       --pid-dir=${RPM_INSTALL_PREFIX3}

%preun
bash ${RPM_INSTALL_PREFIX0}/sbin/update-hadoop-env.sh \
       --prefix=${RPM_INSTALL_PREFIX0} \
       --bin-dir=${RPM_INSTALL_PREFIX0}/bin \
       --sbin-dir=${RPM_INSTALL_PREFIX0}/sbin \
       --conf-dir=${RPM_INSTALL_PREFIX1} \
       --log-dir=${RPM_INSTALL_PREFIX2} \
       --pid-dir=${RPM_INSTALL_PREFIX3} \
       --uninstall

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %__rm -rf $RPM_BUILD_ROOT
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files 
%defattr(-,root,root)
%attr(0755,root,hadoop) %{_log_dir}
%attr(0775,root,hadoop) %{_pid_dir}
%config(noreplace) %{_conf_dir}/configuration.xsl
%config(noreplace) %{_conf_dir}/core-site.xml
%config(noreplace) %{_conf_dir}/hadoop-env.sh
%config(noreplace) %{_conf_dir}/hadoop-metrics.properties
%config(noreplace) %{_conf_dir}/hadoop-metrics2.properties
%config(noreplace) %{_conf_dir}/hadoop-policy.xml
%config(noreplace) %{_conf_dir}/log4j.properties
#%config(noreplace) %{_conf_dir}/masters
#%config(noreplace) %{_conf_dir}/slaves
%{_conf_dir}/ssl-client.xml.example
%{_conf_dir}/ssl-server.xml.example
%{_prefix}

%config(noreplace) %{_conf_dir}/capacity-scheduler.xml
%config(noreplace) %{_conf_dir}/container-executor.cfg
%config(noreplace) %{_conf_dir}/hadoop-env.cmd
%config(noreplace) %{_conf_dir}/hdfs-site.xml
%config(noreplace) %{_conf_dir}/httpfs-env.sh
%config(noreplace) %{_conf_dir}/httpfs-log4j.properties
%config(noreplace) %{_conf_dir}/httpfs-signature.secret
%config(noreplace) %{_conf_dir}/httpfs-site.xml
%config(noreplace) %{_conf_dir}/kms-acls.xml
%config(noreplace) %{_conf_dir}/kms-env.sh
%config(noreplace) %{_conf_dir}/kms-log4j.properties
%config(noreplace) %{_conf_dir}/kms-site.xml
%config(noreplace) %{_conf_dir}/mapred-env.cmd
%config(noreplace) %{_conf_dir}/mapred-env.sh
%config(noreplace) %{_conf_dir}/mapred-queues.xml.template
%config(noreplace) %{_conf_dir}/mapred-site.xml.template
%config(noreplace) %{_conf_dir}/slaves
%config(noreplace) %{_conf_dir}/yarn-env.cmd
%config(noreplace) %{_conf_dir}/yarn-env.sh
%config(noreplace) %{_conf_dir}/yarn-site.xml

