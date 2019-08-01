%define api 0.2
%define major 7
%define libname %mklibname wmf %{api} %{major}
%define litename %mklibname wmflite %{api} %{major}
%define devname %mklibname -d wmf

Summary:	A library to convert wmf files
Name:		libwmf
Version:	0.2.12
Release:	1
License:	GPLv2
Group:		Text tools
Url:		https://github.com/caolanm/libwmf
Source0:	https://github.com/caolanm/libwmf/archive/v%{version}.tar.gz

BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(x11)
Requires(post,postun):	gdk-pixbuf2.0
Requires:	urw-fonts

%description
libwmf is a library for unix like machines that can convert wmf
files into other formats, currently it supports a gd binding
to convert to gif, and an X one to draw direct to an X window
or pixmap.

%package -n %{libname}
Summary:	A library to convert wmf files. - library files
Group:		System/Libraries

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with libwmf.

%package -n %{litename}
Summary:	A library to convert wmf files. - library files
Group:		System/Libraries

%description -n %{litename}
This package contains the library needed to run programs dynamically
linked with libwmflite.

%package -n %{devname}
Summary:	A library to convert wmf files. - development environment
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	libwmf-devel = %{version}-%{release}

%description -n %{devname}
libwmf is a library for unix like machines that can convert wmf
files into other formats, currently it supports a gd binding
to convert to gif, and an X one to draw direct to an X window
or pixmap.

Install libwmf-devel if you need to compile an application with libwmf
support.

%prep
%setup -q

rm -f configure configure.in
autoreconf -fi

%build
%configure \
	--disable-static

%make

%install
%makeinstall_std

mv %{buildroot}%{_prefix}/share/doc/* installed-docs

#gw no windows line endings
perl -pi -e 's/\r//' $(find installed-docs -type f )

# remove anything relevant to fonts.
rm -rf %{buildroot}%{_bindir}/libwmf-fontmap %{buildroot}%{_datadir}/libwmf

%files
%license COPYING
%{_bindir}/wmf2*
%{_libdir}/gdk-pixbuf-2.0/*/loaders/io-wmf.*

%files -n %{libname}
%{_libdir}/libwmf-%{api}.so.%{major}*

%files -n %{litename}
%{_libdir}/libwmflite-%{api}.so.%{major}*

%files -n %{devname}
%doc CREDITS README NEWS ChangeLog
%doc installed-docs/*
%{_bindir}/libwmf-config
%{_libdir}/libwmf.so
%{_libdir}/libwmflite.so
%{_includedir}/libwmf
