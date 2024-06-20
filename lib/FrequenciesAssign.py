class FrequenciesAssign:
    frequencies_2m_fm = [
        "145.275", "145.300", "145.325", "145.350", "145.375",
        "144.525", "144.550", "144.575", "144.625", "144.725","144.750", "144.775",
        "145.400", "145.425", "145.450", "145.475", 
        "145.525", "145.550", "145.200", "145.225", "145.250",
    ]

    def __init__(self, available_frequencies = None, algorithm = "simple"):
        self.available_frequencies = available_frequencies if available_frequencies else FrequenciesAssign.frequencies_2m_fm.copy()
        self.algorithm = algorithm
    
    def generate(self, summits):
        method = getattr(self, self.algorithm, None)
        if callable(method):
            return method(summits)
        else:
            raise ValueError(f"Invalid algorithm: '{self.algorithm}'")

    def simple(self, summits):
        for summit_reference in sorted(summits.keys()):
            if summits[summit_reference].freq:
                print(summit_reference + ": " + summits[summit_reference].freq + " (manually assigned)")
                continue
            if not self.available_frequencies:
                # ToDo: implement freq reuse algorithm
                print("WARNING: no free frequency, reusing frequencies since " + summit_reference)
                self.available_frequencies = FrequenciesAssign.frequencies_2m_fm.copy()
            freq = self.available_frequencies.pop()
            summits[summit_reference].freq = freq
            print(summit_reference + ": " + summits[summit_reference].freq)

        return summits
