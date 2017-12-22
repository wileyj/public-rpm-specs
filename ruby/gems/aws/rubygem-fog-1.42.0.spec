%define filelist %{name}-%{version}-filelist
%global sensu_base %{_sysconfdir}/sensu
%global plugins    %{sensu_base}/plugins
%global metrics    %{sensu_base}/metrics
%global handlers   %{sensu_base}/handlers
%global extensions %{sensu_base}/extensions
%global mutators   %{sensu_base}/mutators

%global gem_name fog
Name: rubygem-fog
Version: 1.42.0
Release: 1.%{dist}
Summary: rubygem fog
Group: Development/Languages
License: MIT
URL: http://github.com/fog/fog
Vendor: %{vendor}
Packager: %{packager}
Requires: ruby rubygems
Provides: rubygem-fog = %{version}
Provides: rubygem(fog) = %{version}
Obsoletes: rubygem-fog < %{version}
Obsoletes: rubygem(fog) < %{version}


Requires: rubygem-fog-aliyun   >= 0.1.0
Requires: rubygem-fog-atmos 
Requires: rubygem-fog-aws   >= 0.6.0
Requires: rubygem-fog-brightbox   = 0.4
Requires: rubygem-fog-cloudatcost   = 0.1.0
Requires: rubygem-fog-core   = 1.45
Requires: rubygem-fog-digitalocean   >= 0.3.0
Requires: rubygem-fog-dnsimple   = 1.0
Requires: rubygem-fog-dynect   = 0.0.2
Requires: rubygem-fog-ecloud   = 0.1
Requires: rubygem-fog-google   <= 0.1.0
Requires: rubygem-fog-internet-archive 
Requires: rubygem-fog-joyent 
Requires: rubygem-fog-json 
Requires: rubygem-fog-local 
Requires: rubygem-fog-openstack 
Requires: rubygem-fog-ovirt 
Requires: rubygem-fog-powerdns   >= 0.1.1
Requires: rubygem-fog-profitbricks 
Requires: rubygem-fog-rackspace 
Requires: rubygem-fog-radosgw   >= 0.0.2
Requires: rubygem-fog-riakcs 
Requires: rubygem-fog-sakuracloud   >= 0.0.4
Requires: rubygem-fog-serverlove 
Requires: rubygem-fog-softlayer 
Requires: rubygem-fog-storm_on_demand 
Requires: rubygem-fog-terremark 
Requires: rubygem-fog-vmfusion 
Requires: rubygem-fog-voxel 
Requires: rubygem-fog-vsphere   >= 0.4.0
Requires: rubygem-fog-xenserver 
Requires: rubygem-fog-xml   = 0.1.1
Requires: rubygem-ipaddress   = 0.5
Requires: rubygem-json   = 2.0


%description
The Ruby cloud services library. Supports all major cloud providers including AWS, Rackspace, Linode, Blue Box, StormOnDemand, and many others. Full support for most AWS services including EC2, S3, CloudWatch, SimpleDB, ELB, and RDS.

%prep
%build
%install
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
gem install --install-dir %{buildroot}/%{gem_dir} --bindir %{buildroot}/%{_bindir} --force --no-rdoc --no-ri --no-doc --ignore-dependencies fog -v %{version}
(
    cd %{buildroot}
    echo '%defattr(-,root,root,-)'
    find %{buildroot} -type d -not \( -path */u/* -o -path */u -o -path */etc -o -path */etc/* -o -path */var -o -path */var/* -prune \) -printf '%%%dir "%p"\n' | %{__sed} -e 's|%{buildroot}||g'
    find %{buildroot} -type f -not \( -path */u/* -o -path */u -o -path */etc -o -path */etc/* -o -path */var -o -path */var/* -prune \) -printf '"%p"\n' | %{__sed} -e 's|%{buildroot}||g'
) >  %{filelist}
sed -i -e 's|%dir ""||g' %{filelist}
%{__sed} -i -e 's/%dir ""//g' %{filelist}
%{__sed} -i -e '/^$/d' %{filelist}

find %{buildroot} -type f -exec sed -i -e 's|/usr/local/bin/ruby|/usr/bin/ruby|g' {} \;

if [[ "%{name}" == *plugins* || "%{name}" == *metrics* || "%{name}" == *mutator* || "%{name}" == *handler* ]]; then
  if [ -d %{buildroot}%{_bindir} ]; then
    for file in `ls %{buildroot}%{_bindir}`
    do
      if [[ $file == metric* ]]; then
        if [ ! -d %{buildroot}%{metrics} ];then
            %__mkdir_p %{buildroot}%{metrics}
        fi
        %{__ln_s} -f %{_bindir}/$file %{buildroot}%{metrics}/$file
        echo "%{metrics}/$file" >> %{filelist}
      elif [[ $file == check* ]]; then
        if [ ! -d %{buildroot}%{plugins} ];then
            %__mkdir_p %{buildroot}%{plugins}
        fi
        %{__ln_s} -f %{_bindir}/$file %{buildroot}%{plugins}/$file
        echo "%{plugins}/$file" >> %{filelist}

      elif [[ $file == mutator* ]]; then
        if [ ! -d %{buildroot}%{mutators} ];then
            %__mkdir_p %{buildroot}%{mutators}
        fi
        %{__ln_s} -f %{_bindir}/$file %{buildroot}%{mutators}/$file
        echo "%{mutators}/$file" >> %{filelist}

      elif [[ $file == handle* ]]; then
        if [ ! -d %{buildroot}%{handlers} ];then
            %__mkdir_p %{buildroot}%{handlers}
        fi
        %{__ln_s} -f %{_bindir}/$file %{buildroot}%{handlers}/$file
        echo "%{handlers}/$file" >> %{filelist}

      else
        if [ ! -d %{buildroot}%{plugins} ];then
            %__mkdir_p %{buildroot}%{plugins}
        fi
        %{__ln_s} -f %{_bindir}/$file %{buildroot}%{plugins}/$file
        echo "%{plugins}/$file" >> %{filelist}
      fi
    done
  fi
fi
exit 0

%clean
[ "%{buildroot}" != "/" ] && %__rm -rf %{buildroot}
[ "%{_builddir}/%{name}-%{version}" != "/" ] && %__rm -rf %{_builddir}/%{name}-%{version}
[ "%{_builddir}/%{filelist}" != "/" ] && %__rm -rf %{_builddir}/%{filelist}
[ "%{_builddir}/%{name}" != "/" ] && %__rm -rf %{_builddir}/%{name}

%files -f %{filelist}

## end file