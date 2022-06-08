function PlotBeampattern(arrayPoints,c, frequenzy)
    SteeringDirection = [0;90];

    microphone = phased.OmnidirectionalMicrophoneElement('FrequencyRange', [20 20e3]);
    rectangularArray = phased.ConformalArray('Element', microphone, 'ElementPosition', transpose(arrayPoints), 'ElementNormal',[90;90]);
    steervec = phased.SteeringVector('SensorArray', rectangularArray, 'PropagationSpeed', c);
    weights = steervec(frequenzy , SteeringDirection);
    [bw, angle] = beamwidth(rectangularArray,20e3,'dBDown',6,'PropagationSpeed',1500)
    %rectangularArray.pattern(frequenzy, 'Weights', weights, 'PropagationSpeed',c,'Type','powerdb','Normalize',true);
end

