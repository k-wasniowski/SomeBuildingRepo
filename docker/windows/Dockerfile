# escape=`

FROM mcr.microsoft.com/powershell:lts-7.2.0-windowsserver-ltsc2022

# Restore the default Windows shell for correct batch processing.
SHELL ["cmd", "/S", "/C"]

ENV MSVC_PATH="C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community" 

USER ContainerAdministrator
RUN pwsh.exe -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SETX PATH "%PATH%;%ALLUSERSPROFILE%\chocolatey\bin" 

RUN choco install --no-progress -y --ignoredetectedreboot 7zip git  python2 python curl sed  windows-sdk-10-version-2004-all`
  && choco install --no-progress -y --ignoredetectedreboot visualstudio2019buildtools --package-parameters "--add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Component.VC.ATLMFC --includeRecommended --nocache --installPath %MSVC_PATH%" || IF "%ERRORLEVEL%"=="3010" EXIT 0

RUN pip install conan

RUN git config --global core.autocrlf false  && git config --global core.filemode false

WORKDIR C:\SomeBuildingRepo

ENTRYPOINT ["powershell.exe"]