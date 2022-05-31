%{
    @title: Acoustic Camera
    @author: Luca Dommel
    @description: An Acoustic Camera with an rectangle Microphone Array
                  using Delay and Sum Algorithm

%}
%% 0.) CONSTANTS
c = 343.2; % speed of sound
frequenzy = 1000;

%% 1. Create Microphone Array via json
fileName = 'data/MicrophoneArrayData.json'; % filename in JSON extension
fid = fopen(fileName); % Opening the file
raw = fread(fid,inf); % Reading the contents
str = char(raw'); % Transformation
fclose(fid); % Closing the file
metaData = jsondecode(str); 
numChannels = length(metaData.elements);
arrayPoints = zeros(numChannels,3);
for m = 1:numChannels
    arrayPoints(m,1) = metaData.elements(m).x;
    arrayPoints(m,2) = metaData.elements(m).y;
    arrayPoints(m,3) = metaData.elements(m).z;
end
xPos = arrayPoints(:,1);
yPos = arrayPoints(:,2);
zPos = zeros(numChannels,1);
scatter(arrayPoints(:,1), arrayPoints(:,2))
title('Microphone Array Geometry (in meter)')

%CalcFrequencys(arrayPoints, c)
%Calculated with the  Method CalcFrequencys(arrayPoints, c);
%calculates minimum and maximum possible spatial samplable frequency
% Method output: MaxFrequenzy: 1372.800000
%                MinFrequenzy: 242.679047

PlotBeampattern(arrayPoints,c, frequenzy);
%calculates beampattern of a steering direction
%   Berechnung des Strahlenmusters für eine bestimmte Array-Geometrie
%    ang = [45;0];
%    SteeringDirection = [90;90];

%PlotCoArray(arrayPoints);
%calculates the Coarray of rectangle 32 mic array




