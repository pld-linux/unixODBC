Summary:	ODBC
Summary(pl):	ODBC
Name:		ODBC
Version:	1.8	
Release:	1
Copyright:	GPL
Group:		Libraries
Group(pl):	Biblioteki
#site:
#path:
BuildRequire:	XFree86-devel
BuildRequire:	qt-devel
Source:		unix%name-%version.tar.gz
Buildroot: /tmp/%{name}-%{version}-root

%define	_prefix	/usr/X11R6

%description

%description -l pl

# optional package =====================
%package devel
Summary:	ODBC
Summary(pl):	ODBC
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki

%description devel
%description -l pl devel

# end of optional package ==============

%prep
%setup -q -n unix%name-%version

%build
./configure --prefix=%{_prefix} \
	--enable-gui \
	--enable-threads \
	--enable-drivers \
	--enable-shared \
	--enable-static \
	--disable-fast-install \
	--with-qt-dir=%{_prefix} 
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
make prefix=$RPM_BUILD_ROOT%{_prefix} install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644, root, root, 755)
%doc
#%attr(,,)

# optional package

%files devel
%defattr(644, root, root, 755)
%doc
#%attr(,,)
#end of optional package

%changelog
* Thu Nov 18 1999 Wojciech "Sas" Ciêciwa <cieciwa@alpha.zarz.agh.edu.pl>
- build RPM.
