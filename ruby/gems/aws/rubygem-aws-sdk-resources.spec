AutoReqProv: no


%define filelist %{name}-%{version}-filelist
%global sensu_base %{_sysconfdir}/sensu
%global plugins    %{sensu_base}/plugins
%global metrics    %{sensu_base}/metrics
%global handlers   %{sensu_base}/handlers
%global extensions %{sensu_base}/extensions
%global mutators   %{sensu_base}/mutators

%global gem_name aws-sdk-resources
Name: rubygem-aws-sdk-resources
Version: 3.10.0
Release: 1.%{dist}
Summary: rubygem aws-sdk-resources
Group: Development/Languages
License: Apache-2.0
URL: http://github.com/aws/aws-sdk-ruby
Vendor: %{vendor}
Packager: %{packager}
Requires: ruby rubygems
Provides: rubygem-aws-sdk-resources = %{version}
Provides: rubygem(aws-sdk-resources) = %{version}
Obsoletes: rubygem-aws-sdk-resources < %{version}
Obsoletes: rubygem(aws-sdk-resources) < %{version}


Requires: rubygem-aws-sdk-acm  = 1
Requires: rubygem-aws-sdk-alexaforbusiness  = 1
Requires: rubygem-aws-sdk-apigateway  = 1
Requires: rubygem-aws-sdk-applicationautoscaling  = 1
Requires: rubygem-aws-sdk-applicationdiscoveryservice  = 1
Requires: rubygem-aws-sdk-appstream  = 1
Requires: rubygem-aws-sdk-appsync  = 1
Requires: rubygem-aws-sdk-athena  = 1
Requires: rubygem-aws-sdk-autoscaling  = 1
Requires: rubygem-aws-sdk-batch  = 1
Requires: rubygem-aws-sdk-budgets  = 1
Requires: rubygem-aws-sdk-cloud9  = 1
Requires: rubygem-aws-sdk-clouddirectory  = 1
Requires: rubygem-aws-sdk-cloudformation  = 1
Requires: rubygem-aws-sdk-cloudfront  = 1
Requires: rubygem-aws-sdk-cloudhsm  = 1
Requires: rubygem-aws-sdk-cloudhsmv2  = 1
Requires: rubygem-aws-sdk-cloudsearch  = 1
Requires: rubygem-aws-sdk-cloudsearchdomain  = 1
Requires: rubygem-aws-sdk-cloudtrail  = 1
Requires: rubygem-aws-sdk-cloudwatch  = 1
Requires: rubygem-aws-sdk-cloudwatchevents  = 1
Requires: rubygem-aws-sdk-cloudwatchlogs  = 1
Requires: rubygem-aws-sdk-codebuild  = 1
Requires: rubygem-aws-sdk-codecommit  = 1
Requires: rubygem-aws-sdk-codedeploy  = 1
Requires: rubygem-aws-sdk-codepipeline  = 1
Requires: rubygem-aws-sdk-codestar  = 1
Requires: rubygem-aws-sdk-cognitoidentity  = 1
Requires: rubygem-aws-sdk-cognitoidentityprovider  = 1
Requires: rubygem-aws-sdk-cognitosync  = 1
Requires: rubygem-aws-sdk-comprehend  = 1
Requires: rubygem-aws-sdk-configservice  = 1
Requires: rubygem-aws-sdk-costandusagereportservice  = 1
Requires: rubygem-aws-sdk-costexplorer  = 1
Requires: rubygem-aws-sdk-databasemigrationservice  = 1
Requires: rubygem-aws-sdk-datapipeline  = 1
Requires: rubygem-aws-sdk-dax  = 1
Requires: rubygem-aws-sdk-devicefarm  = 1
Requires: rubygem-aws-sdk-directconnect  = 1
Requires: rubygem-aws-sdk-directoryservice  = 1
Requires: rubygem-aws-sdk-dynamodb  = 1
Requires: rubygem-aws-sdk-dynamodbstreams  = 1
Requires: rubygem-aws-sdk-ec2  = 1
Requires: rubygem-aws-sdk-ecr  = 1
Requires: rubygem-aws-sdk-ecs  = 1
Requires: rubygem-aws-sdk-efs  = 1
Requires: rubygem-aws-sdk-elasticache  = 1
Requires: rubygem-aws-sdk-elasticbeanstalk  = 1
Requires: rubygem-aws-sdk-elasticloadbalancing  = 1
Requires: rubygem-aws-sdk-elasticloadbalancingv2  = 1
Requires: rubygem-aws-sdk-elasticsearchservice  = 1
Requires: rubygem-aws-sdk-elastictranscoder  = 1
Requires: rubygem-aws-sdk-emr  = 1
Requires: rubygem-aws-sdk-firehose  = 1
Requires: rubygem-aws-sdk-gamelift  = 1
Requires: rubygem-aws-sdk-glacier  = 1
Requires: rubygem-aws-sdk-glue  = 1
Requires: rubygem-aws-sdk-greengrass  = 1
Requires: rubygem-aws-sdk-guardduty  = 1
Requires: rubygem-aws-sdk-health  = 1
Requires: rubygem-aws-sdk-iam  = 1
Requires: rubygem-aws-sdk-importexport  = 1
Requires: rubygem-aws-sdk-inspector  = 1
Requires: rubygem-aws-sdk-iot  = 1
Requires: rubygem-aws-sdk-iotdataplane  = 1
Requires: rubygem-aws-sdk-iotjobsdataplane  = 1
Requires: rubygem-aws-sdk-kinesis  = 1
Requires: rubygem-aws-sdk-kinesisanalytics  = 1
Requires: rubygem-aws-sdk-kinesisvideo  = 1
Requires: rubygem-aws-sdk-kinesisvideoarchivedmedia  = 1
Requires: rubygem-aws-sdk-kinesisvideomedia  = 1
Requires: rubygem-aws-sdk-kms  = 1
Requires: rubygem-aws-sdk-lambda  = 1
Requires: rubygem-aws-sdk-lambdapreview  = 1
Requires: rubygem-aws-sdk-lex  = 1
Requires: rubygem-aws-sdk-lexmodelbuildingservice  = 1
Requires: rubygem-aws-sdk-lightsail  = 1
Requires: rubygem-aws-sdk-machinelearning  = 1
Requires: rubygem-aws-sdk-marketplacecommerceanalytics  = 1
Requires: rubygem-aws-sdk-marketplaceentitlementservice  = 1
Requires: rubygem-aws-sdk-marketplacemetering  = 1
Requires: rubygem-aws-sdk-mediaconvert  = 1
Requires: rubygem-aws-sdk-medialive  = 1
Requires: rubygem-aws-sdk-mediapackage  = 1
Requires: rubygem-aws-sdk-mediastore  = 1
Requires: rubygem-aws-sdk-mediastoredata  = 1
Requires: rubygem-aws-sdk-migrationhub  = 1
Requires: rubygem-aws-sdk-mobile  = 1
Requires: rubygem-aws-sdk-mq  = 1
Requires: rubygem-aws-sdk-mturk  = 1
Requires: rubygem-aws-sdk-opsworks  = 1
Requires: rubygem-aws-sdk-opsworkscm  = 1
Requires: rubygem-aws-sdk-organizations  = 1
Requires: rubygem-aws-sdk-pinpoint  = 1
Requires: rubygem-aws-sdk-polly  = 1
Requires: rubygem-aws-sdk-pricing  = 1
Requires: rubygem-aws-sdk-rds  = 1
Requires: rubygem-aws-sdk-redshift  = 1
Requires: rubygem-aws-sdk-rekognition  = 1
Requires: rubygem-aws-sdk-resourcegroups  = 1
Requires: rubygem-aws-sdk-resourcegroupstaggingapi  = 1
Requires: rubygem-aws-sdk-route53  = 1
Requires: rubygem-aws-sdk-route53domains  = 1
Requires: rubygem-aws-sdk-s3  = 1
Requires: rubygem-aws-sdk-sagemaker  = 1
Requires: rubygem-aws-sdk-sagemakerruntime  = 1
Requires: rubygem-aws-sdk-serverlessapplicationrepository  = 1
Requires: rubygem-aws-sdk-servicecatalog  = 1
Requires: rubygem-aws-sdk-servicediscovery  = 1
Requires: rubygem-aws-sdk-ses  = 1
Requires: rubygem-aws-sdk-shield  = 1
Requires: rubygem-aws-sdk-simpledb  = 1
Requires: rubygem-aws-sdk-sms  = 1
Requires: rubygem-aws-sdk-snowball  = 1
Requires: rubygem-aws-sdk-sns  = 1
Requires: rubygem-aws-sdk-sqs  = 1
Requires: rubygem-aws-sdk-ssm  = 1
Requires: rubygem-aws-sdk-states  = 1
Requires: rubygem-aws-sdk-storagegateway  = 1
Requires: rubygem-aws-sdk-support  = 1
Requires: rubygem-aws-sdk-swf  = 1
Requires: rubygem-aws-sdk-translate  = 1
Requires: rubygem-aws-sdk-waf  = 1
Requires: rubygem-aws-sdk-wafregional  = 1
Requires: rubygem-aws-sdk-workdocs  = 1
Requires: rubygem-aws-sdk-workmail  = 1
Requires: rubygem-aws-sdk-workspaces  = 1
Requires: rubygem-aws-sdk-xray  = 1


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
find %{buildroot} -type f -exec %{__sed} -i -e 's|/usr/local/bin/ruby|/usr/bin/ruby|g' {} \;

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
