Name:                lasso
Version:             2.6.0
Release:             11
Summary:             Liberty Alliance Single Sign On
License:             GPLv2+
URL:                 http://lasso.entrouvert.org/
Source:              http://dev.entrouvert.org/lasso/lasso-%{version}.tar.gz
Requires:            xmlsec1 >= 1.2.25-4
Patch1:              use-specified-python-interpreter.patch
Patch2:              build-scripts-py3-compatible.patch
Patch3:              duplicate-python-LogoutTestCase.patch
patch4:              versioned-python-configure.patch
Patch5:              0005-tests-Remove-the-use-of-an-expired-cert-in-tests-as-.patch
BuildRequires:       autoconf automake check-devel glib2-devel gtk-doc libtool
BuildRequires:       libxml2-devel openssl-devel swig xmlsec1-devel >= 1.2.25-4
BuildRequires:       xmlsec1-openssl-devel >= 1.2.25-4 zlib-devel jpackage-utils
BuildRequires:       java-devel perl(ExtUtils::MakeMaker) perl(strict) perl(Error)
BuildRequires:       perl-devel perl-generators perl(XSLoader) perl(warnings)
BuildRequires:       perl(Test::More) python2-lxml python2-six
BuildRequires:       python2 python2-devel python3 python3-devel
BuildRequires:       python3-lxml python3-six libtool-ltdl-devel

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

%package -n python2-lasso
%{?python_provide:%python_provide python2-lasso}
Summary:             Liberty Alliance Single Sign On (lasso) Python bindings
Requires:            python2 lasso = %{version}-%{release}
Provides:            lasso-python = %{version}-%{release}
Obsoletes:           lasso-python < %{version}-%{release}

%description -n python2-lasso
The package provide Python language bindings for the lasso
(Liberty Alliance Single Sign On)library.

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

%build
./autogen.sh
%configure --enable-php5=no --with-python=%{__python2}
cd lasso
%make_build CFLAGS="%{optflags}"
cd -
cd bindings/python
%make_build CFLAGS="%{optflags}"
make check
mkdir py2
mv lasso.py .libs/_lasso.so py2
cd -
make clean
%configure --enable-php5=no --with-python=%{__python3}
%make_build CFLAGS="%{optflags}"

%check
make check

%install
%make_install exec_prefix=%{_prefix}
%delete_la
find %{buildroot} -type f -name '*.a' -exec rm -f {} \;
install -d -m 0755 %{buildroot}/%{python2_sitearch}
install -m 0755 bindings/python/py2/_lasso.so %{buildroot}/%{python2_sitearch}
install -m 0644 bindings/python/py2/lasso.py %{buildroot}/%{python2_sitearch}
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
%{_libdir}/java/libjnilasso.so
%{_javadir}/lasso.jar

%files -n python2-lasso
%{python2_sitearch}/{lasso.py*,_lasso.so}

%files -n python3-lasso
%{python3_sitearch}/{lasso.py*,_lasso.so,__pycache__/*}

%files help
%doc AUTHORS NEWS README

%changelog
* Wed Jun 18 2020 yaokai <yaoaki13@huawei.com> - 2.6.0-11
- package init