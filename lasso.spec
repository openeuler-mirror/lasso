Name:                lasso
Version:             2.8.0
Release:             2
Summary:             Liberty Alliance Single Sign On
License:             GPLv2+
URL:                 http://lasso.entrouvert.org/
Source:              http://dev.entrouvert.org/lasso/lasso-%{version}.tar.gz
Requires:            xmlsec1 >= 1.2.25-4
Patch1:              Use-OpenSSL-EVP-API-to-work-around-deprecation-of-low.patch

BuildRequires:       autoconf automake check-devel glib2-devel gtk-doc libtool
BuildRequires:       libxml2-devel openssl-devel swig xmlsec1-devel >= 1.2.25-4
BuildRequires:       xmlsec1-openssl-devel >= 1.2.25-4 zlib-devel jpackage-utils
BuildRequires:       java-1.8.0-openjdk-devel perl(ExtUtils::MakeMaker) perl(strict) perl(Error)
BuildRequires:       perl-devel perl-generators perl(XSLoader) perl(warnings)
BuildRequires:       perl(Test::More) python3 python3-devel
BuildRequires:       python3-lxml python3-six libtool-ltdl-devel

Obsoletes:           java-lasso < %{version}-%{release}

%description
The package is a implements the Liberty Alliance Single Sign On standards library,
includeing the SAML2 and SAML specifications. it provides bindings for multiple
languages.and allows to handle the whole life-cycle of SAML based Federations.

%package devel
Summary:             Provide the development headers and documentation for lasso
Requires:            lasso = %{version}-%{release}
%description devel
The devel packages contains the header files, develpoment documentation
and static libraries for lasso.

%package -n perl-lasso
Summary:             Liberty Alliance Single Sign On (lasso) Perl bindings
Requires:            perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:            lasso = %{version}-%{release}
%description -n perl-lasso
The package provide Perl language bindings for the lasso
(Liberty Alliance Single Sign On) library.

%package -n java-lasso
Summary:             Liberty Alliance Single Sign On (lasso) Java bindings
Requires:            java-headless jpackage-utils lasso = %{version}-%{release}
Provides:            lasso-java = %{version}-%{release}
Obsoletes:           lasso-java < %{version}-%{release}
%description -n java-lasso
The package provide Java language bindings for the lasso
(Liberty Alliance Single Sign On) library.

%package -n python3-lasso
%{?python_provide:%python_provide python3-lasso}
Summary:             Liberty Alliance Single Sign On (lasso) Python bindings
Requires:            python3 lasso = %{version}-%{release}

%description -n python3-lasso
The package provide Python language bindings for the lasso
(Liberty Alliance Single Sign On)library.

%package help
Summary:             Help document for the lasso packages

%description help
Help document for the lasso packages

%prep
%autosetup -n lasso-%{version} -p1
sed -i -E -e '/^#![[:blank:]]*(\/usr\/bin\/env[[:blank:]]+python[^3]?\>) \
|(\/usr\/bin\/python[^3]?\>)/d' `grep -r -l -E '^#![[:blank:]]*(/usr/bin/python[^3]?) \
|(/usr/bin/env[[:blank:]]+python[^3]?)' *`
aclocal
automake --add-missing

%build
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
./autogen.sh
%configure --enable-php5=no --with-python=%{__python3}
%if "%toolchain" == "clang"
	%make_build CFLAGS="%{optflags} -Wno-error=int-conversion"
%else 
	%make_build CFLAGS="%{optflags}"
%endif

%check
make check CK_TIMEOUT_MULTIPLIER=10

%install
%make_install exec_prefix=%{_prefix} DESTDIR=%{buildroot}
chmod u+w %{buildroot}/usr/lib64/perl5/vendor_perl/auto/Lasso/Lasso.so
find %{buildroot} -type f -name '*.la' -exec rm -f {} \;
find %{buildroot} -type f -name '*.a' -exec rm -f {} \;
find %{buildroot} \( -name perllocal.pod -o -name .packlist \) -exec rm -v {} \;
find %{buildroot}/usr/lib*/perl5 -type f -print |
  sed "s@^%{buildroot}@@g" > lasso-perl-filelist
if [ "$(cat lasso-perl-filelist)X" = "X" ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit -1
fi
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%{_libdir}/liblasso.so.3*
%exclude %{_defaultdocdir}/lasso

%files devel
%{_includedir}/lasso
%{_libdir}/{liblasso.so,pkgconfig/lasso.pc}

%files -n perl-lasso -f lasso-perl-filelist

%files -n java-lasso

%files -n python3-lasso
%{python3_sitearch}/{lasso.py*,_lasso.so,__pycache__/*}

%files help
%doc AUTHORS NEWS README

%changelog
* Thu May 11 2023 yoo <sunyuechi@iscas.ac.cn> - 2.8.0-2
- fix clang build error, automake version

* Wed Feb 08 2023 Ge Wang <wangge20@h-partners.com> - 2.8.0-1
- Update to version 2.8.0 fix build failure due to openssl update to version 3.0.8

* Fri Apr 8 2022 yaoxin <yaoxin30@h-partners.com> - 2.7.0-1
- Resolve compilation failures

* Sat Jul 10 2021 shixuantong <shixuantong@huawei.com> - 2.6.0-13
- fix CVE-2021-28091

* Wed Oct 21 2020 Ge Wang <wangge20@huawei.com> - 2.6.0-12
- remove python2

* Wed Jun 18 2020 yaokai <yaoaki13@huawei.com> - 2.6.0-11
- package init
