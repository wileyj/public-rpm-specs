%define _find_requires 0
%define real_name mahout
Name:          apache-mahout
Version:       0.11.1
Release:       1.%{dist}
Summary:       Apache Mahout
Group:         System Environment/Daemons
URL:           http://mahout.apache.org/core
License:       ASL 2.0
Vendor: %{vendor}
Packager: %{packager}
BuildArch:     noarch
Source:        %{real_name}.tar.gz
BuildRoot:     %{_tmppath}/%{real_name}-%{version}-%{release}-root-%(%{__id} -un)
Requires(pre): shadow-utils
Requires:      jdk

%define _unpackaged_files_terminate_build 0
%define _missing_doc_files_terminate_build 0
# No debug package:


%description
Apache Mahout is a scalable machine learning library that supports large data sets.

%prep
%setup -q -n %{real_name}

%build
git pull

%install
export DONT_STRIP=1
%{__rm} -rf %{buildroot}
%{__install} -m 0755 -d %{buildroot}/opt/%{real_name}
for D in $(find . -mindepth 1 -maxdepth 1 -type d | cut -c 3- | %{__grep} -Evw 'build|docs|src')
do
  %{__cp} -a $D %{buildroot}/opt/%{real_name}/
done
#%{__install} -m 0644 *.jar %{buildroot}/opt/%{real_name}/
#%{__install} -m 0644 *.war %{buildroot}/opt/%{real_name}/
%{__install} -m 0755 -d %{buildroot}/var/run/mahout
%{__install} -m 0755 -d %{buildroot}/var/log/mahout

# Packing list
( cd %{buildroot}
  echo '%defattr(-,root,root,-)'
  echo '%attr(0755,mahout,mahout) /var/run/mahout'
  echo '%attr(0755,mahout,mahout) /var/log/mahout'
  find %{buildroot}/opt/%{real_name} -type d -printf '%%%dir %p\n' | %{__sed} -e 's|%{buildroot}||g'
  find %{buildroot}/opt/%{real_name} -type f -printf '%p\n' | %{__grep} -v 'conf/' | %{__sed} -e 's|%{buildroot}||g'
  find %{buildroot}/opt/%{real_name}/conf -type f -printf '%%%config(noreplace) %p\n' | %{__sed} -e 's|%{buildroot}||g'
) > filelist

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}

%pre
getent group mahout >/dev/null || \
  lgroupadd -r mahout
getent passwd mahout >/dev/null || \
  luseradd -m -r -g mahout -c 'HDFS runtime user' -s /bin/bash mahout
exit 0

%check

%post

%preun

%files -f filelist

%changelog
