################################################################################
#
# Copyright (C) 2019 Team Deep-Data, Colorado School of Mines
#
# Date created: 1/22/19
# Date last updated:
#
# Creators:
#   - Sean Smith            seansmith@mines.edu
#   - Tyler Murphy          tmurphy@mines.edu
#   - Tyler Blount          trblount@mines.edu
#   - Sydney Nelson         snelson1@mines.edu
#   - Josh Grego            jgrego@mines.edu
#   - Jake Steiner          msteiner@mines.edu
#   - Marcelo Gonzales      magonzal@mines.edu
#   - Daniel Hanuszczak     danielhanuszczak@mines.edu
#
################################################################################


Included below are file descriptions for all files in deep_data_package module
along will descriptions of functionality.


################################################################################
###                              file_reader.py                              ###
################################################################################

    Module for reading AVIRIS flight data and mapping

# OVERVIEW =====================================================================

    Classes ====================================================================
        hyperion_band_reader
        aviris_band_reader
        pickled_aviris_band_reader

    Functions ==================================================================
        select_closest_band
        create_pickled_aviris_flight
        get_available_aviris_flights
        get_available_pickled_aviris_flights
        get_available_hyperion_passes



# CLASS hyperion_band_reader ===================================================

      Class for reading Hyperion data from GEOtiff L1 files

      NOTE: bands 1-70 and VNIR, bands 71-242 are SWIR

    Reference ==================================================================
        https://archive.usgs.gov/archive/sites/eo1.usgs.gov/EO1userguidev2pt320030715UC.pdf
        https://crisp.nus.edu.sg/~research/tutorial/eo1.htm
        https://crisp.nus.edu.sg/~research/tutorial/eo1.htm

    Inputs =====================================================================
        Optional:
            hyperion_pass - name of Hyperion pass to load (Default EO1H0410362008289110KF)
            scale_factor - number to divide bands by (Defaul 80 to get radiance values)

    Returns ====================================================================
        class to load radiance bands as np arrays

    class Attributes ===========================================================
        band_reader.hyperion_pass - Hyperion flight loaded
        band_reader.scale_factor - number to divide bands by (Defaul 80 to get radiance values)
        band_reader.mode - self identified mode for reference ('hyperion')
        band_reader.approx_band_centers - string refence to what band centers correspond to what files in Hyperion GEOtif files
        self.swir_actual_band_centers - caluclated band centers for SWIR bands (for reference)


    METHODS ====================================================================

        load_band ==============================================================
            By defualt loads Hyperion pass EO1H0410362008289110KF over sunshine canyon
            landfill

            Reference ==========================================================
                N/A

            Inputs =============================================================
                band_req - band wavelength to load
                adjust_for_gain - N/A

            Returns ============================================================
                2D np array of radiance data for band wavelength called

                - To load a row

                    band_array[row_number, :]

                - To load a column

                    band_array[:, col_number]

                - To load a pixel

                    band_array[row_number, col_number]


        load_pixel =============================================================
            Function for reading all bands of an individual pixel from AVIRIS
            flight data

            Reference ==========================================================
                N/A

            Inputs =============================================================
                row - int of row number of requested pixel
                col - int of column number of requested pixel
                adjust_for_gain - N/A

            Returns ==========================================================
                Ordered dict of wavelengths vs irradiance for requested pixel



# CLASS aviris_band_reader =====================================================

      Class for reading AVIRIS flight data from uncompressed AVIRIS flight
      folder. No files need to be modified after downloading from AVIRIS data
      portal. Just uncompress in the aviris_flight_folder and go.

      By defualt loads AVIRIS flight f111115t01p00r08 over sunshine canyon
      landfill

    Reference ==============================================================
        N/A

    Inputs =================================================================
        Optional:
            aviris_flight_number - AVIRIS flight number to load
            aviris_filename - filename to load in AVIRIS flight number folder
            samples - from hdr file in AVERIS flight folder (Defualt 780)
            lines - from hdr file in AVERIS flight folder (Defualt 8355)
            bands - from hdr file in AVERIS flight folder (Defualt 224)
            aviris_calibration_filename - name of AVIRIS file for reflectance calibration
            aviris_gain_filename - name of AVIRIS gain file for reflectance calibration

    Returns ================================================================
        class to load radiance bands as np arrays

    class Attributes =======================================================
        band_reader.aviris_flight -  AVIRIS flight loaded
        band_reader.n_cols - number of columns in AVIRIS band file (equals input samples)
        band_reader.n_rows - number of rows in AVIRIS band file (equals input lines)
        band_reader.n_bands - number of bands in AVIRIS band file (equals input bands)
        band_reader.scale_factor - multiplier of bands (equals input scale_factor)
        band_reader.aviris_flight_folder_filepath - full filepath for AVIRIS flight folder
        band_reader.bands_filepath - full filepath for AVIRIS band file

        band_reader.info - dict with useful info from AVIRIS flight
            Contains:
                # General info
                ['info']['n_rows'] = number of rows in .npy files
                ['info']['n_cols'] = number of columns in .npy files
                ['info']['n_bands'] = number of bands from AVIRIS flight
                ['info']['AVIRIS_flight'] = aviris_flight

                # Band info
                ['band_calibration']['band_quantity'] = 'Wavelength'
                ['band_calibration']['band_unit'] = 'nm'
                ['band_calibration']['centers'] = mathmatical center of wavelength
                ['band_calibration']['bandwidths'] = bandwidths of wavelengths
                ['band_calibration']['bands'] = wavelengths callable

                # Gain values
                ['gain_values'] = np array of gain values for each band

            Call any of above w/ band_reader.info['INSERT_AS_SHOWN_ABOVE']

    METHODS ====================================================================

        parse_aviris_flight ====================================================
            Function for loading AVIRIS flight files of the first time
            By defualt loads AVIRIS flight f111115t01p00r08 over sunshine canyon landfill

            Inputs =============================================================
                info_file_name - name for info file to be written by parser
                aviris_calibration_filename - name of AVIRIS file for reflectance calibration
                aviris_gain_filename - name of AVIRIS gain file for reflectance calibration

            Returns ============================================================
                flight_dict - dict with useful info from AVIRIS flight
                    Contains:
                        # General info
                        ['info']['n_rows'] = number of rows in .npy files
                        ['info']['n_cols'] = number of columns in .npy files
                        ['info']['n_bands'] = number of bands from AVIRIS flight
                        ['info']['AVIRIS_flight'] = aviris_flight

                        # Band info
                        ['band_calibration']['band_quantity'] = 'Wavelength'
                        ['band_calibration']['band_unit'] = 'nm'
                        ['band_calibration']['centers'] = mathmatical center of wavelength
                        ['band_calibration']['bandwidths'] = bandwidths of wavelengths
                        ['band_calibration']['bands'] = wavelengths callable

                        # Gain values
                        ['gain_values'] = np array of gain values for each band


        get_memmap =============================================================
            Function for loading memmap of AVIRIS band file

            Inputs =============================================================
                N/A

            Returns ============================================================
                np.memmap of AVIRIS band file


        load_band ==============================================================
            Function for reading AVIRIS flight data from .npy files pickled by
            create_pickled_aviris_flight()

            By defualt loads AVIRIS flight f111115t01p00r08 over sunshine canyon
            landfill

            Reference ==========================================================
                N/A

            Inputs =============================================================
                band_req - band wavelength to load
                adjust_for_gain - If want to divide band array by gain value in .gain file (Default: False)

            Returns ============================================================
                2D np array of radiance data for band wavelength called

                - To load a row

                    band_array[row_number, :]

                - To load a column

                    band_array[:, col_number]

                - To load a pixel

                    band_array[row_number, col_number]


        load_pixel =============================================================
            Function for reading all bands of an individual pixel from AVIRIS
            flight data

            Reference ==========================================================
                N/A

            Inputs =============================================================
                row - int of row number of requested pixel
                col - int of column number of requested pixel
                adjust_for_gain - N/A

            Returns ============================================================
                Ordered dict of wavelengths vs irradience for requested pixel



# CLASS pickled_aviris_band_reader =============================================

      Class for reading AVIRIS flight data from .npy files pickled by
      create_pickled_aviris_flight()

      By defualt loads AVIRIS flight f111115t01p00r08 over sunshine canyon
      landfill

    Reference ==============================================================
        N/A

    Inputs =================================================================
        Optional:
            aviris_flight - AVIRIS flight to load

    Returns ================================================================
        class to load radiance bands as np arrays

    class Attributes =======================================================
        band_reader.aviris_flight -  AVIRIS flight loaded
        band_reader.np_path - path will load .npy files from

        band_reader.info - dict with useful info from AVIRIS flight
            Contains:
                # General info
                ['info']['n_rows'] = number of rows in .npy files
                ['info']['n_cols'] = number of columns in .npy files
                ['info']['n_bands'] = number of bands from AVIRIS flight
                ['info']['AVIRIS_flight'] = aviris_flight

                # Band info
                ['band_calibration']['band_quantity'] = 'Wavelength'
                ['band_calibration']['band_unit'] = 'nm'
                ['band_calibration']['centers'] = mathmatical center of wavelength
                ['band_calibration']['bandwidths'] = bandwidths of wavelengths
                ['band_calibration']['bands'] = wavelengths callable

                # Gain values
                ['gain_values'] = np array of gain values for each band

            Call any of above w/ band_reader.info['INSERT_AS_SHOWN_ABOVE']

    METHODS ====================================================================

        load_band ==============================================================
            Function for reading AVIRIS flight data from .npy files pickled by
            create_pickled_aviris_flight()

            Reference ==========================================================
                N/A

            Inputs =============================================================
                band_req - band wavelength to load

            Returns ============================================================
                2D np array of radiance data for band wavelength called

                - To load a row

                    band_array[row_number, :]

                - To load a column

                    band_array[:, col_number]

                - To load a pixel

                    band_array[row_number, col_number]


        load_pixel =============================================================
            Function for reading all bands of an individual pixel from AVIRIS
            flight data from .npy files pickled by create_pickled_aviris_flight()

            Reference ==========================================================
                N/A

            Inputs =============================================================
                row - int of row number of requested pixel
                col - int of column number of requested pixel
                adjust_for_gain - N/A

            Returns ============================================================
                Ordered dict of wavelengths vs irradience for requested pixel



# FUNCTION select_closest_band =================================================

    Returns closest band available to band_req.

    Inputs =============================================================
        band_req - band wavelength to match
        band_req - list of band wavelengths available

    Returns ============================================================
        band available, if two numbers are equally close, returns the
        smallest number.



# FUNCTION create_pickled_aviris_flight ========================================

    Function for creating pickled AVIRIS flight data using spectral python library

    By defualt loads AVIRIS flight f111115t01p00r08 over sunshine canyon landfill

    Reference ==============================================================
        N/A

    Inputs =================================================================
        Optional:
            aviris_flight - AVIRIS flight number
            aviris_flight_folder - AVIRIS flight folder to load
            aviris_bands_filename - filename to load in AVIRIS flight number folder
            samples - from hdr file in AVERIS flight folder (Defualt 780)
            lines - from hdr file in AVERIS flight folder (Defualt 8355)
            bands - from hdr file in AVERIS flight folder (Defualt 224)
            aviris_calibration_filename - name of AVIRIS file for reflectance calibration
            aviris_gain_filename - name of AVIRIS gain file for reflectance calibration
            adjust_for_gain - if should devide bands by associated gain value to true values (Default False)
            scale_factor - if want to dived all values by some value (Default 10000.0)

    Returns ================================================================
        N/A



# FUNCTION get_available_aviris_flights ========================================

    Function listing all AVIRIS flights available

    Inputs =================================================================
        N/A

    Returns ================================================================
        List of AVIRIS flights available



# FUNCTION get_available_pickled_aviris_flights ================================

    Function listing all pickled AVIRIS flights available

    Inputs =================================================================
        N/A

    Returns ================================================================
        List of pickled AVIRIS flights available



# FUNCTION get_available_hyperion_passes =======================================

    Function listing all Hyperion passes available

    Inputs =================================================================
        N/A

    Returns ================================================================
        List of Hyperion passes available



################################################################################



################################################################################
###                                 mapper.py                                ###
################################################################################

    Module for mapping band ratio output arrays

# OVERVIEW =====================================================================

    Functions ==================================================================
        create_heatmap_interactive



# FUNCTION create_heatmap_interactive ==========================================

    Function for creating an interactive heatmap

    Reference ==============================================================
        N/A

    Inputs =================================================================
        band_reader - band_reader class instance
        bandratio_array - bandratio result array for heatmap
        bandratio_array_name - name of bandratio calculated
        flight_name - name of the flight
        alpha - transparency value of overlay (Defualt 0.6)
        gamma_1 - threshold value for map (Default mean of normalized bandratio_array)
        interval - step value of threshold slider (Default 0.00001)
        std_multiplier - multiplier of std for range of values of threshold slider (Default 3)
        clipped - if want clipped heatmap instead of default treshhold (Default False)
        display - show plt (Default True)
        save - save plt when (Default False)
        cmap - color scheme for heatmap (Default 'hot' for threshold, 'jet' for clipped)
        quiet - if should not log info about bandratio_array (Defualt False)
        rgb_scale_value - float value to increase brightness of rgb image

    Returns ================================================================
        N/A



################################################################################



################################################################################
###                              band_ratios.py                              ###
################################################################################

    Module for calculating band ratios

# OVERVIEW =====================================================================

    Functions ==================================================================
      Deep_Data
      HI_1453
      HI_1215
      HI_1732
      GM
      NDVI
      NDPI



# FUNCTION Deep_Data ===========================================================

    Deep-Data Hydrocarbon Index ================================================
        Convert numpy arrays of radiance data to a Deep-Data hydrocarbon
        index map

    Inputs =====================================================================
        L_1197 : At-sensor radiance at 1197 nm wavelength (numpy array)
        L_1216 : At-sensor radiance at 1216 nm wavelength (numpy array)
        L_1235 : At-sensor radiance at 1235 nm wavelength (numpy array)
        L_1373 : At-sensor radiance at 1373 nm wavelength (numpy array)
        L_1453 : At-sensor radiance at 1453 nm wavelength (numpy array)
        L_1503 : At-sensor radiance at 1503 nm wavelength (numpy array)

    Returns ====================================================================
        Deep-Data Hydrocarbon Index Map



# FUNCTION HI_1453 =============================================================

    1453 Hydrocarbon Index =====================================================
        Convert numpy arrays of radiance data to a 1453 hydrocarbon index map

    Inputs =====================================================================
        L_1373 : At-sensor radiance at 1373 nm wavelength (numpy array)
        L_1453 : At-sensor radiance at 1453 nm wavelength (numpy array)
        L_1503 : At-sensor radiance at 1503 nm wavelength (numpy array)

    Returns ====================================================================
        1453 Hydrocarbon Index Map



# FUNCTION HI_1215 =============================================================

    1215 Hydrocarbon Index =====================================================
        Convert numpy arrays of radiance data to a 1215 hydrocarbon index map

    Inputs =====================================================================
        L_1197 : At-sensor radiance at 1197 nm wavelength (numpy array)
        L_1216 : At-sensor radiance at 1216 nm wavelength (numpy array)
        L_1235 : At-sensor radiance at 1235 nm wavelength (numpy array)

    Returns ====================================================================
        1215 Hydrocarbon Index Map



# FUNCTION HI_1732 =============================================================

    1732 Hydrocarbon Index =================================================
        Convert numpy arrays of radiance data to a 1732 hydrocarbon index map

    Inputs =====================================================================
        L_1705 : At-sensor radiance at 1705 nm wavelength (numpy array)
        L_1729 : At-sensor radiance at 1729 nm wavelength (numpy array)
        L_1741 : At-sensor radiance at 1741 nm wavelength (numpy array)

    Returns ====================================================================
        1732 Hydrocarbon Index Map



# FUNCTION GM ==================================================================

    Goddijn-Murphy Index =======================================================
        From: "Proof of concept for a model of light reflectance of plastics
        floating on natural waters" by Lonneke Goddijn-Murphy and Juvenal
        Dufaur. - See Table 5

        Convert numpy arrays of radiance data to a Goddijn-Murphy map

    Inputs =====================================================================
        L_850 : At-sensor radiance at 850 nm wavelength (numpy array)
        L_1660 : At-sensor radiance at 1660 nm wavelength (numpy array)

    Returns ====================================================================
        Goddijn-Murphy Map



# FUNCTION NDVI ================================================================

    NDVI =======================================================================
        Convert numpy arrays of radiance data to a NDVI map

    Inputs =====================================================================
        L_1006 : At-sensor radiance at 1006 nm wavelength (numpy array)
        L_675 : At-sensor radiance at 675 nm wavelength (numpy array)

    Returns ====================================================================
        NDVI Map



# FUNCTION NDPI ================================================================

    NDPI =======================================================================
        Convert numpy arrays of radiance data to a NDPI map

    Inputs =====================================================================
        L_1263 : At-sensor radiance at 1263 nm wavelength (numpy array)
        L_2417 : At-sensor radiance at 2417 nm wavelength (numpy array)

    Returns ====================================================================
        NDPI Map



################################################################################
