AutoReqProv: no
%global alinux_ruby 24
%global ruby_ver 2.4
%global gem_dir %{gem24_dir}


%define filelist %{name}-%{version}-filelist
%global sensu_base %{_sysconfdir}/sensu
%global plugins    %{sensu_base}/plugins
%global metrics    %{sensu_base}/metrics
%global handlers   %{sensu_base}/handlers
%global extensions %{sensu_base}/extensions
%global mutators   %{sensu_base}/mutators

%global gem_name fog
Name: rubygem%{alinux_ruby}-fog
Version: 1.32.0
Release: 1.%{dist}
Summary: rubygem fog
Group: Development/Languages
License: MIT
URL: http://github.com/fog/fog
Vendor: %{vendor}
Packager: %{packager}
Requires: ruby%{alinux_ruby} rubygems%{alinux_ruby}
Provides: rubygem%{alinux_ruby}-fog = %{version}
Provides: rubygem%{alinux_ruby}(fog) = %{version}
Obsoletes: rubygem%{alinux_ruby}-fog < %{version}
Obsoletes: rubygem%{alinux_ruby}(fog) < %{version}


Requires: rubygem%{alinux_ruby}-fog-atmos
Requires: rubygem%{alinux_ruby}-fog-aws  >= 0.6.0
Requires: rubygem%{alinux_ruby}-fog-brightbox  = 0.4
Requires: rubygem%{alinux_ruby}-fog-core  = 1.32
Requires: rubygem%{alinux_ruby}-fog-ecloud  = 0.1.1
Requires: rubygem%{alinux_ruby}-fog-google  >= 0.0.2
Requires: rubygem%{alinux_ruby}-fog-json
Requires: rubygem%{alinux_ruby}-fog-local
Requires: rubygem%{alinux_ruby}-fog-powerdns  >= 0.1.1
Requires: rubygem%{alinux_ruby}-fog-profitbricks
Requires: rubygem%{alinux_ruby}-fog-radosgw  >= 0.0.2
Requires: rubygem%{alinux_ruby}-fog-riakcs
Requires: rubygem%{alinux_ruby}-fog-sakuracloud  >= 0.0.4
Requires: rubygem%{alinux_ruby}-fog-serverlove
Requires: rubygem%{alinux_ruby}-fog-softlayer
Requires: rubygem%{alinux_ruby}-fog-storm_on_demand
Requires: rubygem%{alinux_ruby}-fog-terremark
Requires: rubygem%{alinux_ruby}-fog-vmfusion
Requires: rubygem%{alinux_ruby}-fog-voxel
Requires: rubygem%{alinux_ruby}-fog-xml  = 0.1.1
Requires: rubygem%{alinux_ruby}-ipaddress  = 0.5
Requires: rubygem%{alinux_ruby}-nokogiri  >= 1.5.11,


%description
The Ruby cloud services library. Supports all major cloud providers including AWS, Rackspace, Linode, Blue Box, StormOnDemand, and many others. Full support for most AWS services including EC2, S3, CloudWatch, SimpleDB, ELB, and RDS.

%prep
%build
%install
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
gem install --install-dir %{buildroot}/%{gem_dir} --bindir %{buildroot}/%{_bindir} --force --no-rdoc --no-ri --no-doc --ignore-dependencies %{gem_name} -v %{version}
%{__perl} -MFile::Find -le '
    find ({ wanted => \&wanted, no_chdir => 1}, "%{buildroot}");
    for my $x (sort @dirs, @files) {
        push @ret, $x unless indirs($x);
    }
    print join "\n", sort @ret;
    sub wanted {
        return if /auto$/;
        local $_ = $File::Find::name;
        my $f = $_; s|^\Q%{buildroot}\E||;
        return unless length;
        return $files[@files] = $_ if -f $f;
        $d = $_;
        /\Q$d\E/ && return for reverse sort @INC;
        $d =~ /\Q$_\E/ && return
            for qw|/etc %_prefix/man %_prefix/bin %_prefix/share|;
        $dirs[@dirs] = $_;
      }

    sub indirs {
        my $x = shift;
        $x =~ /^\Q$_\E\// && $x ne $_ && return 1 for @dirs;
    }
' > $RPM_BUILD_DIR/%{filelist}
%__sed -i -e 's/.*/\"&\"/g' $RPM_BUILD_DIR/%{filelist}
find %{buildroot} -type f -exec %{__sed} -i -e 's|/usr/local/bin/ruby|/usr/bin/ruby%{ruby_ver}|g' {} \;

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
