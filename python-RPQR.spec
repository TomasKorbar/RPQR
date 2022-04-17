Name:           python-RPQR
Version:        1.0.0
Release:        1%{?dist}
Summary:        RPM Package Query Resolver

License:        GPLv3
URL:            https://github.com/TomasKorbar/RPQR
Source0:        RPQR.tgz

BuildArch:      noarch
Requires:       python3 python3-dnf
BuildRequires:  python3-devel sed python3-wheel

%global _description %{expand:
RPQR is an originally proposed tool which is supposed to make maintainers life easier by
allowing them to describe how to acquire the data only once and then being able to retrieve
it on demand. It is flexible enough to store any new kind of data and to search packages
based on combination of any of them while also providing the option to accelerate queries
by making specialized commands. RPQR also lets users build a cache which makes further
queries faster and thus saves time while doing everyday work.}

%description %_description

%package -n python3-RPQR
Summary:        %{summary}

%description -n python3-RPQR %_description

%prep
%setup -q -n RPQR

%generate_buildrequires

%build
%pyproject_wheel

%install
sed -i "s;\\./rpqr/loader/plugins/implementations;%{python3_sitelib}/rpqr/loader/plugins/implementations;g" example.conf
mkdir -m 0755 -p %{buildroot}/%{_sysconfdir}
install -m 0644 -vp example.conf            %{buildroot}/%{_sysconfdir}/rpqr.conf
mkdir -m 0755 -p %{buildroot}/%{_mandir}/man1/
install -m 0644 -vp RPQR.1                  %{buildroot}/%{_mandir}/man1/
%pyproject_install

%check
true

%files -n python3-RPQR
%license LICENSE
/%{_mandir}/man1/RPQR.1.*
%{python3_sitelib}/rpqr
%{python3_sitelib}/rpqr-%{version}.dist-info
%{_bindir}/RPQR
%{_bindir}/RPQROrphaned
%{_sysconfdir}/rpqr.conf
%ghost /var/tmp/rpqr.json

%changelog
* Thu Mar 10 2022 Tomas Korbar <tkorbar@redhat.com> - 1.0.0-1
- Initial package
