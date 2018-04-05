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

%global gem_name aws-sdk-resources
Name: rubygem%{alinux_ruby}-aws-sdk-resources
Version: 3.10.0
Release: 1.%{dist}
Summary: rubygem aws-sdk-resources
Group: Development/Languages
License: Apache-2.0
URL: http://github.com/aws/aws-sdk-ruby
Vendor: %{vendor}
Packager: %{packager}
Requires: ruby%{alinux_ruby} rubygems%{alinux_ruby}
Provides: rubygem%{alinux_ruby}-aws-sdk-resources = %{version}
Provides: rubygem%{alinux_ruby}(aws-sdk-resources) = %{version}
Obsoletes: rubygem%{alinux_ruby}-aws-sdk-resources < %{version}
Obsoletes: rubygem%{alinux_ruby}(aws-sdk-resources) < %{version}


Requires: rubygem%{alinux_ruby}-aws-sdk-acm  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-alexaforbusiness  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-apigateway  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-applicationautoscaling  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-applicationdiscoveryservice  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-appstream  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-appsync  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-athena  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-autoscaling  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-batch  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-budgets  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-cloud9  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-clouddirectory  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-cloudformation  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-cloudfront  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-cloudhsm  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-cloudhsmv2  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-cloudsearch  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-cloudsearchdomain  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-cloudtrail  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-cloudwatch  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-cloudwatchevents  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-cloudwatchlogs  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-codebuild  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-codecommit  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-codedeploy  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-codepipeline  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-codestar  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-cognitoidentity  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-cognitoidentityprovider  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-cognitosync  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-comprehend  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-configservice  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-costandusagereportservice  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-costexplorer  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-databasemigrationservice  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-datapipeline  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-dax  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-devicefarm  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-directconnect  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-directoryservice  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-dynamodb  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-dynamodbstreams  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-ec2  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-ecr  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-ecs  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-efs  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-elasticache  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-elasticbeanstalk  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-elasticloadbalancing  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-elasticloadbalancingv2  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-elasticsearchservice  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-elastictranscoder  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-emr  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-firehose  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-gamelift  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-glacier  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-glue  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-greengrass  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-guardduty  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-health  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-iam  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-importexport  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-inspector  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-iot  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-iotdataplane  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-iotjobsdataplane  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-kinesis  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-kinesisanalytics  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-kinesisvideo  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-kinesisvideoarchivedmedia  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-kinesisvideomedia  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-kms  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-lambda  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-lambdapreview  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-lex  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-lexmodelbuildingservice  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-lightsail  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-machinelearning  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-marketplacecommerceanalytics  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-marketplaceentitlementservice  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-marketplacemetering  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-mediaconvert  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-medialive  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-mediapackage  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-mediastore  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-mediastoredata  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-migrationhub  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-mobile  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-mq  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-mturk  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-opsworks  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-opsworkscm  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-organizations  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-pinpoint  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-polly  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-pricing  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-rds  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-redshift  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-rekognition  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-resourcegroups  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-resourcegroupstaggingapi  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-route53  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-route53domains  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-s3  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-sagemaker  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-sagemakerruntime  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-serverlessapplicationrepository  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-servicecatalog  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-servicediscovery  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-ses  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-shield  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-simpledb  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-sms  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-snowball  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-sns  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-sqs  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-ssm  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-states  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-storagegateway  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-support  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-swf  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-translate  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-waf  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-wafregional  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-workdocs  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-workmail  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-workspaces  = 1
Requires: rubygem%{alinux_ruby}-aws-sdk-xray  = 1


%description
The official AWS SDK for Ruby. Provides both resource oriented interfaces and API clients for AWS services.

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
