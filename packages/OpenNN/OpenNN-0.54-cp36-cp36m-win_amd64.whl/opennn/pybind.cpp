// System includes

#include <iostream>
#include <stdio.h>
#include <string>
#include <fstream>
#include <algorithm>
#include <functional>
#include <limits>
#include <cmath>
#include <ctime>
#include <cstdlib>
#include <sstream>
#include <cassert>
#include <iomanip>
#include <iterator>
#include <istream>
#include <map>
#include <numeric>
#include <ostream>
#include <stdexcept>
#include <vector>
#include <climits>
#include <time.h>

// Pybind includes

#include <pybind11/eigen.h>
#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <pybind11/stl.h>

// OpenNN includes

#include "../../opennn/opennn.h"

// Namespaces

using namespace OpenNN;
using namespace std;
namespace py = pybind11;

// OpenNN module

PYBIND11_MODULE(opennn, m) {

    // Data set

    py::class_<DataSet> dataSet(m, "DataSet");
    
	dataSet.doc() = R"pbdoc(
		This class represents the concept of data set for data modelling problems, such as function regression, classification and time series prediction. It basically consists of a data matrix plus a variables and an instances objects.)pbdoc";

    dataSet.def(py::init<>(), "Default initialization method. It creates a data set object with zero instances and zero inputs and target variables. It also initializes the rest of class members to their default values.")
        .def(py::init<const Eigen::MatrixXd&>(), "Data constructor. It creates a data set object from a data matrix. It also initializes the rest of class members to their default values. @param data Data matrix.")
        .def(py::init<const size_t&, const size_t&>(), "Instances and variables number constructor. It creates a data set object with given instances and variables numbers. All the variables are set as inputs. It also initializes the rest of class members to their default values. @param new_instances_number Number of instances in the data set. @param new_variables_number Number of variables.")
        .def(py::init<const size_t&, const size_t&, const size_t&>(), "Instances number, input variables number and target variables number constructor. It creates a data set object with given instances and inputs and target variables numbers. It also initializes the rest of class members to their default values. @param new_instances_number Number of instances in the data set. @param new_inputs_number Number of input variables. @param new_targets_number Number of target variables.")
        .def(py::init<const string&>(), "File constructor. It creates a data set object by loading the object members from a data file. Please mind about the file format. This is specified in the User's Guide. @param data_file_name Data file file name.")
		.def(py::init<const string&, const string&>(), "File and separator initialization method. It creates a data set object by loading the object members from a data file. It also sets a separator. Please mind about the file format. This is specified in the User's Guide. @param data_file_name Data file file name. @param separator Data file file name.")
        .def(py::init<const DataSet&>(), "Copy constructor. It creates a copy of an existing inputs targets data set object. @param other_data_set Data set object to be copied.")
        .def(py::self == py::self, "")
        .def("variables", (const Variables& (DataSet::*) () const) &DataSet::get_variables, "Returns a constant reference to the variables object composing this data set object.")
        .def("set_data_file_name", (void (DataSet::*) (const string&)) &DataSet::set_data_file_name, "Sets the name of the data file. It also loads the data from that file. Moreover, it sets the variables and instances objects. @param new_data_file_name Name of the file containing the data.")
		.def("set_separator", (void (DataSet::*) (const string&))&DataSet::set_separator, "Sets a new separator from a string. @param new_separator String with the separator value.")
        .def("load_data", &DataSet::load_data, "This method loads the data file.")
        .def("print_data", &DataSet::print_data, "Prints to the sceen the values of the data matrix.")
        .def("scale_inputs_minimum_maximum", &DataSet::scale_inputs_minimum_maximum_eigen, "Scales the input variables with the calculated minimum and maximum values from the data matrix. It updates the input variables of the data matrix. It also returns a vector of vectors with the minimum and maximum values of the input variables.")
        .def("scale_targets_minimum_maximum", &DataSet::scale_targets_minimum_maximum_eigen, "Scales the target variables with the calculated minimum and maximum values from the data matrix. It updates the target variables of the data matrix. It also returns a vector of vectors with the statistics of the input target variables.")
        .def("instances", &DataSet::get_instances, "Returns a constant reference to the instances object composing this data set object.")
        .def("data", &DataSet::get_data_eigen, "Returns a reference to the data matrix in the data set. The number of rows is equal to the number of instances. The number of columns is equal to the number of variables.")
		.def("training_data", &DataSet::get_training_data_eigen, "Returns a matrix with the training instances in the data set. The number of rows is the number of training instances. The number of columns is the number of variables.")
		.def("selection_data", &DataSet::get_selection_data_eigen, "Returns a matrix with the selection instances in the data set. The number of rows is the number of selection instances. The number of columns is the number of variables.")
		.def("testing_data", &DataSet::get_testing_data_eigen, "Returns a matrix with the testing instances in the data set. The number of rows is the number of testing instances. The number of columns is the number of variables.")
		.def("inputs_eigen", &DataSet::get_inputs_eigen, "Returns a matrix with the input variables in the data set. The number of rows is the number of instances. The number of columns is the number of input variables.")
		.def("targets_eigen", &DataSet::get_targets_eigen, "Returns a matrix with the target variables in the data set. The number of rows is the number of instances. The number of columns is the number of target variables.")
		.def("training_inputs", &DataSet::get_training_inputs_eigen, "Returns a matrix with training instances and input variables. The number of rows is the number of training instances. The number of columns is the number of input variables.")
		.def("training_targets", &DataSet::get_training_targets_eigen, "Returns a matrix with training instances and target variables. The number of rows is the number of training instances. The number of columns is the number of target variables.")
		.def("selection_inputs", &DataSet::get_selection_inputs_eigen, "Returns a matrix with selection instances and input variables. The number of rows is the number of selection instances. The number of columns is the number of input variables.")
		.def("selection_targets", &DataSet::get_selection_targets_eigen, "Returns a matrix with selection instances and target variables. The number of rows is the number of selection instances. The number of columns is the number of target variables.")
		.def("testing_inputs", &DataSet::get_testing_inputs_eigen, "Returns a matrix with testing instances and input variables. The number of rows is the number of testing instances. The number of columns is the number of input variables.")
		.def("testing_targets", &DataSet::get_testing_targets_eigen, "Returns a matrix with testing instances and target variables. The number of rows is the number of testing instances. The number of columns is the number of target variables.")
		.def("set_variable_use", (void (DataSet::*) (const size_t&, const string&)) &DataSet::set_variable_use, "Set the use for a variable in the DataSet. @param i Index of the variable. @param new_use New use fr the variable.")
		.def("input_target_correlations", &DataSet::calculate_input_target_correlations_eigen, "Calculates the linear correlations between all outputs and all inputs. It returns a matrix with number of rows the targets number and number of columns the inputs number. Each element contains the linear correlation between a single target and a single output.");
		

    // Variables

    py::class_<Variables> variables(m, "Variables");

    variables.doc() = "This class is used to store information about the variables of a data set. Variables in a data set can be used as inputs and targets. This class also stores information about the name, unit and description of all the variables.";

    variables.def(py::init<>(), "Default initialization method. It creates a variables object with zero variables. It also initializes the rest of class members to their default values.")
        .def(py::init<const size_t&>(), "Variables number constructor. It creates a variables object with a given number of variables. All the variables are set as inputs but the last, which is set as targets. It also initializes the rest of class members to their default values. @param new_variables_number Number of variables.")
        .def(py::init<const size_t&, const size_t&>(), "Variables number initialization method. It creates a variables object with a given number of input and target variables. It also initializes the rest of class members to their default values. @param new_inputs_number Number of input variables. @param new_targets_number Number of target variables.")
        .def(py::init<const Variables&>(), "Copy initialization method. It creates a copy of an existing variables object. @param other_variables Variables object to be copied.")
        .def(py::self == py::self, "")
        .def("variables_number", &Variables::get_variables_number, "Returns the total number of variables in the data set.")
        .def("inputs_number", &Variables::get_inputs_number, "Returns the number of input variables of the data set.")
        .def("targets_number", &Variables::get_targets_number, "Returns the number of target variables of the data set.")
        .def("inputs_name", &Variables::get_inputs_name_std, "Returns the names of the input variables in the data set.")
        .def("targets_name", &Variables::get_targets_name_std, "Returns the names of the target variables in the data set.")
        .def("inputs_information", &Variables::get_inputs_information_vector_of_vector, "Returns the inputs information.")
        .def("targets_information", &Variables::get_targets_information_vector_of_vector, "Returns the targets information.")
        .def("set_use", (void (Variables::*) (const size_t&, const string&)) &Variables::set_use, "Sets the use of a single variable from a string. The possible values for that string are 'Unused', 'Input' and 'Target'. @param i Index of variable. @param new_use Use for that variable.")
        .def("set_name", (void (Variables::*) (const size_t&, const string&)) &Variables::set_name, "This method set the name of a single variable. If the vector of names is zero the rest of elements are initialized as empty strings. @param i Index of variable. @param new_name Name of variable.")
        .def("set_units", (void (Variables::*) (const size_t&, const string&)) &Variables::set_units, "This method set the units of a single variable. If the vector of units is zero the rest of elements are initialized as empty strings. @param i Index of variable. @param new_units Units of variable.");


    // Instances

    py::class_<Instances> instances(m, "Instances");

    instances.doc() = "This class is used to store information about the instances of a data set. Instances in a data set can be used for training, selection and testing.";

    instances.def(py::init<>(), "Default initialization method. It creates a instances object with zero instances. It also initializes the rest of class members to their default values.")
        .def(py::init<const size_t&>(), "Instances number initialization method. It creates a data set object with a given number of instances. It also initializes the rest of class members to their default values. @param new_instances_number Number of instances in the data set.")
        .def(py::init<const Instances&>(), "Copy initialization method. It creates a copy of an existing instances object. @param other_instances Instances object to be copied.")
        .def(py::self == py::self, "")
        .def("instances_number", &Instances::get_instances_number, "Returns the number of instances in the data set.")
        .def("training_instances_number", &Instances::get_training_instances_number, "Returns the number of instances in the data set which will be used for training.")
        .def("selection_instances_number", &Instances::get_selection_instances_number, "Returns the number of instances in the data set which will be used for selection.")
        .def("testing_instances_number", &Instances::get_testing_instances_number, "Returns the number of instances in the data set which will be used for testing.")
        .def("set_all_training", (void (Instances::*) ()) &Instances::set_training, "Sets all the instances in the data set for training.");

		
    // Neural network

    py::class_<NeuralNetwork> neuralNetwork(m, "NeuralNetwork");

    neuralNetwork.doc() = "This class represents the concept of neural network in the OpenNN library. A neural network here is defined as a multilayer perceptron extended with a scaling layer, an unscaling layer, a bounding layer and a probabilistic layer. This neural network is used to span a function space for the variational problem at hand.";

    neuralNetwork.def(py::init<>(), "Default initialization method.")
        .def(py::init<const MultilayerPerceptron&>(), "Multilayer Perceptron initialization method. It creates a neural network object from a given multilayer perceptron. The rest of pointers are initialized to nullptr. This initialization method also initializes the rest of class members to their default values.")
        .def(py::init<const vector<size_t>&>(), "Multilayer perceptron architecture initialization method. It creates a neural network object with a multilayer perceptron given by its architecture. This initialization method allows an arbitrary deep learning architecture. The rest of pointers are initialized to nullptr. This initialization method also initializes the rest of class members to their default values. @param new_multilayer_perceptron_architecture Vector with the number of inputs and the numbers of perceptrons in each layer. The size of this vector must be equal to one plus the number of layers.")
        .def(py::init<const size_t&, const size_t&>(), "One layer initialization method. It creates a one-layer perceptron object. The number of independent parameters is set to zero. The multilayer perceptron parameters are initialized at random. @param new_inputs_number Number of inputs in the layer. @param new_perceptrons_number Number of perceptrons in the layer.")
        .def(py::init<const size_t&, const size_t&, const size_t&>(), "Two layers initialization method. It creates a neural network object with a two layers perceptron. The rest of pointers of this object are initialized to nullptr. The other members are initialized to their default values. @param new_inputs_number Number of inputs in the multilayer perceptron. @param new_hidden_perceptrons_number Number of neurons in the hidden layer of the multilayer perceptron. @param new_output_perceptrons_number Number of outputs neurons.")
        .def(py::init<const string&>(), "File initialization method. It creates a neural network object by loading its members from an XML-type file. Please be careful with the format of that file, which is specified in the OpenNN manual. @param file_name Name of neural network file.")
        .def(py::init<const NeuralNetwork&>(), "Copy initialization method. It creates a copy of an existing neural network object. @param other_neural_network Neural network object to be copied.")
        .def(py::self == py::self, "")
        .def("inputs", &NeuralNetwork::get_inputs_pointer, "Returns a pointer to the inputs object composing this neural network.")
        .def("outputs", &NeuralNetwork::get_outputs_pointer, "Returns a pointer to the outputs object composing this neural network.")
        .def("construct_scaling_layer", (void (NeuralNetwork::*) ()) &NeuralNetwork::construct_scaling_layer, "This method constructs a scaling layer within the neural network. The size of the scaling layer is the number of inputs in the multilayer perceptron.")
		.def("construct_scaling_layer", (void (NeuralNetwork::*) (const Vector<Statistics<double>>&)) &NeuralNetwork::construct_scaling_layer, "This method constructs a scaling layer within the neural network. The size of the scaling layer is the number of inputs in the multilayer perceptron. @param input_statistics Inputs Statistics vector.")
		.def("construct_scaling_layer", (void (NeuralNetwork::*) (const Eigen::MatrixXd&)) &NeuralNetwork::construct_scaling_layer, "")
        .def("get_scaling_layer", &NeuralNetwork::get_scaling_layer_pointer, "Returns a pointer to the scaling layer composing this neural network.")
        .def("construct_unscaling_layer", (void (NeuralNetwork::*) ()) &NeuralNetwork::construct_unscaling_layer, "This method constructs an unscaling layer within the neural network. The size of the unscaling layer is the number of outputs in the multilayer perceptron.")
		.def("construct_unscaling_layer", (void (NeuralNetwork::*) (const Vector<Statistics<double>>&)) &NeuralNetwork::construct_unscaling_layer, "This method constructs a scaling layer within the neural network. The size of the scaling layer is the number of inputs in the multilayer perceptron. @param target_statistics Targets Statistics vector.")
		.def("construct_unscaling_layer", (void (NeuralNetwork::*) (const Eigen::MatrixXd&)) &NeuralNetwork::construct_unscaling_layer, "")
        .def("get_unscaling_layer", &NeuralNetwork::get_unscaling_layer_pointer, "Returns a pointer to the unscaling layer composing this neural network.")
		.def("write_expression", &NeuralNetwork::write_expression, "Writes the mathematical expression of the model.")
		.def("write_expression_python", &NeuralNetwork::write_expression_python, "Writes the mathematical expression of the model in Python format.")
		.def("save_parameters", (void (NeuralNetwork::*) (const string&)) &NeuralNetwork::save_parameters, "Saves to a data file the parameters of a neural network object. @param file_name Name of parameters data file.")
		.def("load_parameters", (void (NeuralNetwork::*) (const string&)) &NeuralNetwork::load_parameters, "Loads the multilayer perceptron parameters from a data file. The format of this file is just a sequence of numbers. @param file_name Name of parameters data file.")
		.def("save_expression", (void (NeuralNetwork::*) (const string&)) &NeuralNetwork::save_expression, "Saves the mathematical expression represented by the neural network to a text file. @param file_name Name of expression text file.")
		.def("save_expression_python", (void (NeuralNetwork::*) (const string&)) &NeuralNetwork::save_expression_python, "Saves the python function of the expression represented by the neural network to a text file. @param file_name Name of expression text file.")
		.def("save_expression_R", (void (NeuralNetwork::*) (const string&)) &NeuralNetwork::save_expression_R, "Saves the R function of the expression represented by the neural network to a text file. @param file_name Name of expression text file.")
		.def("save", (void (NeuralNetwork::*) (const string&)) &NeuralNetwork::save, "Saves to a XML file the members of a neural network object. @param file_name Name of neural network XML file.")
		.def("load", (void (NeuralNetwork::*) (const string&)) &NeuralNetwork::load, "Loads from a XML file the members for this neural network object. Please mind about the file format, which is specified in the User's Guide. @param file_name Name of neural network XML file.")
		.def("calculate_outputs", (Eigen::MatrixXd (NeuralNetwork::*) (const Eigen::MatrixXd&)) &NeuralNetwork::calculate_outputs_eigen, "Calculates the outputs vector from the multilayer perceptron in response to an inputs vector. @param inputs Set of inputs to the neural network.")
		.def("parameters_norm", &NeuralNetwork::calculate_parameters_norm, "Returns the norm of the vector of parameters.")
		.def("initialize_random", &NeuralNetwork::initialize_random, "Initializes the neural network at random. This is useful for testing purposes.")
		.def("randomize_parameters_normal", (void (NeuralNetwork::*) ()) &NeuralNetwork::randomize_parameters_normal, "Initializes all the parameters in the neural newtork(biases and synaptic weiths + independent parameters) at random with values chosen from a normal distribution with mean 0 and standard deviation 1.")
		.def("randomize_parameters_uniform", (void (NeuralNetwork::*) ()) &NeuralNetwork::randomize_parameters_uniform, "Initializes all the parameters in the newtork(biases and synaptic weiths + independent parameters) at random with values comprised between -1 and +1.");
		
		
	// Multilayer perceptron
	
	py::class_<MultilayerPerceptron> multilayerPerceptron(m, "MultilayerPerceptron");
	
	multilayerPerceptron.doc() = "This class represents the concept of multilayer perceptron. A multilayer perceptron is a feed-forward network of layers of perceptrons. This is the most important class included in the definition of a neural network.";
	
	multilayerPerceptron.def(py::init<>(), "Default constructor. It creates a multilayer perceptron object witout any layer. This constructor also initializes the rest of class members to their default values.");
	
	
	// Perceptron layer
	
	py::class_<PerceptronLayer> perceptronLayer(m, "PerceptronLayer");
	
	perceptronLayer.doc() = "This class represents a layer of perceptrons. Layers of perceptrons will be used to construct multilayer perceptrons.";
	
	perceptronLayer.def(py::init<>(), "Default constructor. It creates a empty layer object, with no perceptrons. This constructor also initializes the rest of class members to their default values.");

		
    // Inputs
	
    py::class_<Inputs> inputs(m, "Inputs");

    inputs.doc() = "This class is used to store some information about the input variables of a neural network. That information basically consists of the names, units and descriptions of the input variables.";

    inputs.def(py::init<>(), "Default constructor. It creates an inputs object with zero inputs.")
        .def(py::init<const size_t&>(), "Inputs number constructor. It creates an inputs object with given numbers of inputs. This constructor initializes the members of the object to their default values. @param new_inputs_number Number of inputs.")
        .def(py::init<const Inputs&>(), "Copy constructor. It creates a copy of an existing inputs object. @param other_inputs Inputs object to be copied.")
        .def(py::self == py::self, "")
        .def("set_information", &Inputs::set_information_vector_of_vector, "Sets all the possible information about the input variables. The format is a vector of vectors of size three (Name of input variables, Units of input variables, Description of input variables). @param new_information Input variables information.");

		
    // Outputs

    py::class_<Outputs> outputs(m, "Outputs");

    outputs.doc() = "This class is used to store some information about the output variables of a neural network. That information basically consists of the names, units and descriptions of the output variables.";

    outputs.def(py::init<>(), "Default constructor. It creates a outputs information object with zero outputs.")
        .def(py::init<const size_t&>(), "Outputs number constructor. It creates a outputs object with a given number of outputs. This constructor initializes the members of the object to their default values. @param new_outputs_number Number of outputs.")
        .def(py::init<const Outputs&>(), "Copy constructor. It creates a copy of an existing outputs object. @param other_outputs Outputs object to be copied.")
        .def(py::self == py::self, "")
        .def("set_information", &Outputs::set_information_vector_of_vector, "Sets all the possible information about the output variables. The format is a vector of vectors of size three: (Name of output variables, Units of output variables, Description of output variables). @param new_information Output variables information.");

		
    // ScalingLayer

    py::class_<ScalingLayer> scalingLayer(m, "ScalingLayer");

    scalingLayer.doc() = "This class represents a layer of scaling neurons. Scaling layers are included in the definition of a neural network. They are used to normalize variables so they are in an appropriate range for computer processing.";

    scalingLayer.def(py::init<>(), "Default constructor. It creates a scaling layer object with no scaling neurons.")
        .def(py::init<const size_t&>(), "Scaling neurons number constructor. This constructor creates a scaling layer with a given size. The members of this object are initialized with the default values. @param new_scaling_neurons_number Number of scaling neurons in the layer.")
		.def(py::init<const Vector< Statistics<double> >&>(), "Statistics initialization method. This initialization method creates a scaling layer with given minimums, maximums, means and standard deviations. The rest of members of this object are initialized with the default values. @param new_statistics Vector of vectors with the variables statistics.")
		.def(py::init<const ScalingLayer&>(), "Copy constructor.")
        .def(py::self == py::self, "")
        .def("set_statistics", &ScalingLayer::set_statistics_eigen, "Sets all the scaling layer statistics from a vector statistics structures. The size of the vector must be equal to the number of scaling neurons in the layer. @param new_statistics Scaling layer statistics.")
        .def("set_scaling_methods", (void (ScalingLayer::*) (const string&)) &ScalingLayer::set_scaling_methods, "Sets all the methods to be used for scaling with the given method. The argument is a string containing the name of the method('NoScaling', 'MeanStandardDeviation' or 'MinimumMaximum'). @param new_scaling_methods_string New scaling methods for the variables.");

		
    // UnscalingLayer

    py::class_<UnscalingLayer> unscalingLayer(m, "UnscalingLayer");

    unscalingLayer.doc() = "This class represents a layer of unscaling neurons. Unscaling layers are included in the definition of a neural network. They are used to unnormalize variables so they are in the original range after computer processing.";

    unscalingLayer.def(py::init<>(), "Default constructor.")
        .def(py::init<const size_t&>(), "Outputs number constructor.")
		.def(py::init<const Vector< Statistics<double> >&>(), "Statistics initialization method. This initialization method creates an unscaling layer with given minimums, maximums, means and standard deviations. The rest of members of this object are initialized with the default values. @param new_statistics Vector of vectors with the variables statistics.")
		.def(py::init<const UnscalingLayer&>(), "Copy constructor.")
        .def(py::self == py::self, "")
        .def("set_statistics", &UnscalingLayer::set_statistics_eigen, "Sets the statistics for all the neurons in the unscaling layer from a vector. The size of this vector must be equal to the number of unscaling neurons. @param new_statistics Unscaling neurons statistics.")
        .def("set_unscaling_method", (void (UnscalingLayer::*) (const string&)) &UnscalingLayer::set_unscaling_method, "Sets the method to be used for unscaling the outputs from the multilayer perceptron. The argument is a string containing the name of the method('NoUnscaling', 'MeanStandardDeviation', 'MinimumMaximum' or 'Logarithmic'). @param new_unscaling_method New unscaling method for the output variables.");


    // Training strategy

    py::class_<TrainingStrategy> trainingStrategy(m, "TrainingStrategy");

    trainingStrategy.doc() = "This class represents the concept of training strategy for a neural network.";

    trainingStrategy.def(py::init<>(), "Default initialization method. It creates a training strategy object not associated to any loss index object. It also constructs the main optimization algorithm object.")
        .def(py::init<NeuralNetwork*, DataSet*>(), "Neural Network and Data Set initialization method. It creates a training strategy object associated to NeuralNetwork and DataSet objects. @param neural_network NeuralNetwrk object. @param data_set DataSet object.")
        .def(py::init<const string&>(), "File initialization method. It creates a training strategy object associated to a loss index object. It also loads the members of this object from a XML file. @param file_name Name of training strategy XML file.")
        .def("set_loss_method", (void (TrainingStrategy::*) (const string&)) &TrainingStrategy::set_loss_method, "Select a loss function to use in the Neural Network training. @param new_method New loss method to use: (SUM_SQUARED_ERROR, MEAN_SQUARED_ERROR, NORMALIZED_SQUARED_ERROR, MINKOWSKI_ERROR, WEIGHTED_SQUARED_ERROR, CROSS_ENTROPY_ERROR)")
        .def("set_training_method", (void (TrainingStrategy::*) (const string&)) &TrainingStrategy::set_training_method, "Sets a new main optimization algorithm from a string containing the type. @param new_training_method String with the type of main optimization algorithm (GRADIENT_DESCENT, CONJUGATE_GRADIENT, QUASI_NEWTON_METHOD, LEVENBERG_MARQUARDT_ALGORITHM, STOCHASTIC_GRADIENT_DESCENT, ADAPTIVE_MOMENT_ESTIMATION).")
        .def("train", &TrainingStrategy::perform_training_void, "This is the most important method of this class. It optimizes the loss index of a neural network. This method also returns a structure with the results from training.")
		.def("get_gradient_descent", &TrainingStrategy::get_gradient_descent_pointer, "Returns a pointer to the gradient descent main algorithm. It also throws an exception if that pointer is nullptr.")
		.def("get_conjugate_gradient", &TrainingStrategy::get_conjugate_gradient_pointer, "Returns a pointer to the conjugate gradient main algorithm. It also throws an exception if that pointer is nullptr.")
		.def("get_quasi_newton_method", &TrainingStrategy::get_quasi_Newton_method_pointer, "Returns a pointer to the quasi Newton method main algorithm. It also throws an exception if that pointer is nullptr.")
		.def("get_stochastic_gradient_descent", &TrainingStrategy::get_stochastic_gradient_descent_pointer, "Returns a pointer to the stochastic gradient descent main algorithm. It also throws an exception if that pointer is nullptr.")
		.def("get_levenberg_marquardt_algorithm_pointer", &TrainingStrategy::get_Levenberg_Marquardt_algorithm_pointer, "Returns a pointer to the Levenberg Marquardt algorithm main algorithm. It also throws an exception if that pointer is nullptr.");
		

    // Model selection

    py::class_<ModelSelection> modelSelection(m, "ModelSelection");

    modelSelection.doc() = "This class represents the concept of model selection algorithm. It is used for finding a network architecture with maximum selection capabilities.";

    modelSelection.def(py::init<>(), "Default initialization method.")
        .def(py::init<TrainingStrategy*>(), "Training strategy initialization method. @param new_training_strategy_pointer Pointer to a training strategy object.")
        .def(py::init<const string&>(), "File initialization method. @param file_name Name of XML model selection file.")
        .def("set_order_selection_method", (void (ModelSelection::*) (const string&)) &ModelSelection::set_order_selection_method, "Sets a new order selection algorithm from a string. @param new_order_selection_method String with the order selection type.")
        .def("set_inputs_selection_method", (void (ModelSelection::*) (const string&)) &ModelSelection::set_inputs_selection_method, "Sets a new inputs selection algorithm from a string. @param new_inputs_selection_method String with the inputs selection type.")
        .def("perform_order_selection", &ModelSelection::perform_order_selection, "Perform the order selection, returns a structure with the results of the order selection. It also set the neural network of the training strategy pointer with the optimum parameters.")
        .def("perform_inputs_selection", &ModelSelection::perform_inputs_selection, "Perform the inputs selection, returns a structure with the results of the inputs selection. It also set the neural network of the training strategy pointer with the optimum parameters.");

		
    // Testing analysis

    py::class_<TestingAnalysis> testingAnalysis(m, "TestingAnalysis");

    testingAnalysis.doc() = "This class contains tools for testing neural networks in different learning tasks. In particular, it can be used for testing function regression, classification or time series prediction problems.";

    testingAnalysis.def(py::init<>(), "Default initialization method. It creates a testing analysis object neither associated to a neural network nor to a mathematical model or a data set. By default, it constructs the function regression testing object.")
        .def(py::init<NeuralNetwork*, DataSet*>(), "Neural network and data set initialization method. It creates a testing analysis object associated to a neural network and to a data set. By default, it constructs the function regression testing object. @param new_neural_network_pointer Pointer to a neural network object. @param new_data_set_pointer Pointer to a data set object.")
        .def(py::init<const string&>(), "File initialization method. It creates a testing analysis object neither associated to a neural network nor to a mathematical model or a data set. It also loads the members of this object from XML file. @param file_name Name of testing analysis XML file.")
		.def("perform_linear_regression_analysis", &TestingAnalysis::perform_linear_regression_analysis_void, "Perform a linear regression between predicted and actual values for target variables.")
		.def("linear_regression_correlations", &TestingAnalysis::get_linear_regression_correlations_std, "Get the linear regression correlation for the target variables.");


    // TRAINING METHODS
	
	// QuasiNewtonMethod

    py::class_<QuasiNewtonMethod> quasiNewtonMethod(m, "QuasiNewtonMethod");

	quasiNewtonMethod.doc() = "This concrete class represents a quasi-Newton training algorithm for a loss index of a neural network.";
	
	quasiNewtonMethod.def(py::init<>(), "Default initialization method. It creates a quasi-Newton method optimization algorithm not associated to any loss index. It also initializes the class members to their default values.")
        .def(py::init<LossIndex*>(), "Loss index initialization method. It creates a quasi-Newton method optimization algorithm associated to a loss index. It also initializes the class members to their default values. @param new_loss_index_pointer Pointer to a loss index object.")
        .def(py::init<const tinyxml2::XMLDocument&>(), "XML initialization method. It creates a quasi-Newton method optimization algorithm not associated to any loss index. It also initializes the class members to their default values.")
        .def("set_display_period", (void (QuasiNewtonMethod::*) (const size_t&)) &QuasiNewtonMethod::set_display_period, "Sets a new number of epochs between the training showing progress. @param Number of epochs between the training showing progress.")
		.def("set_max_epochs", (void (QuasiNewtonMethod::*) (const size_t&)) &QuasiNewtonMethod::set_maximum_epochs_number, "Sets a new maximum number of epochs number. @param new_maximum_epochs_number Maximum number of epochs in which the selection evalutation decreases.")
		.def("set_loss_goal", (void (QuasiNewtonMethod::*) (const double&)) &QuasiNewtonMethod::set_loss_goal, "Sets a new goal value for the loss. This is used as a stopping criterion when training a multilayer perceptron. @param new_loss_goal Goal value for the loss.")
		.def("set_max_time", (void (QuasiNewtonMethod::*) (const double&)) &QuasiNewtonMethod::set_maximum_time, "Sets a new maximum training time. @param new_maximum_time Maximum training time.")
		.def("set_minimum_loss_decrease", (void (QuasiNewtonMethod::*) (const double&)) &QuasiNewtonMethod::set_minimum_loss_decrease, "Sets a new minimum loss improvement during training. @param new_minimum_loss_increase Minimum improvement in the loss between two epochs.");


    // GradientDescent

    py::class_<GradientDescent> gradientDescent(m, "GradientDescent");
        
	gradientDescent.doc() = "This concrete class represents the gradient descent optimization algorithm for a loss index of a neural network.";
	
	gradientDescent.def(py::init<>(), "Default initialization method. It creates a gradient descent optimization algorithm not associated to any loss index object. It also initializes the class members to their default values.")
        .def(py::init<LossIndex*>(), "Loss index initialization method. It creates a gradient descent optimization algorithm associated to a loss index. It also initializes the class members to their default values. @param new_loss_index_pointer Pointer to a loss index object.")
        .def(py::init<const tinyxml2::XMLDocument&>(), "XML initialization method. It creates a gradient descent optimization algorithm not associated to any loss index object. It also loads the class members from a XML document. @param document TinyXML document with the members of a gradient descent object.")
        .def("set_display_period", (void (GradientDescent::*) (const size_t&)) &GradientDescent::set_display_period, "Sets a new number of epochs between the training showing progress. @param Number of epochs between the training showing progress.")
		.def("set_max_epochs", (void (GradientDescent::*) (const size_t&)) &GradientDescent::set_maximum_epochs_number, "Sets a new maximum number of epochs number. @param new_maximum_epochs_number Maximum number of epochs in which the selection evalutation decreases.")
		.def("set_loss_goal", (void (GradientDescent::*) (const double&)) &GradientDescent::set_loss_goal, "Sets a new goal value for the loss. This is used as a stopping criterion when training a multilayer perceptron. @param new_loss_goal Goal value for the loss.")
		.def("set_max_time", (void (GradientDescent::*) (const double&)) &GradientDescent::set_maximum_time, "Sets a new maximum training time. @param new_maximum_time Maximum training time.")
		.def("set_minimum_loss_decrease", (void (GradientDescent::*) (const double&)) &GradientDescent::set_minimum_loss_decrease, "Sets a new minimum loss improvement during training. @param new_minimum_loss_increase Minimum improvement in the loss between two epochs.");


    // ConjugateGradient

    py::class_<ConjugateGradient> conjugateGradient(m, "ConjugateGradient");
        
	conjugateGradient.doc() = "This concrete class represents a conjugate gradient training algorithm for a loss index of a neural network.";
	
	conjugateGradient.def(py::init<>(), "Default initialization method. It creates a conjugate gradient optimization algorithm object not associated to any loss index object. It also initializes the class members to their default values.")
        .def(py::init<LossIndex*>(), "General initialization method. It creates a conjugate gradient optimization algorithm associated to a loss index object. It also initializes the rest of class members to their default values. @param new_loss_index_pointer Pointer to a loss index object.")
        .def(py::init<const tinyxml2::XMLDocument&>(), "XML initialization method. It creates a conjugate gradient optimization algorithm not associated to any loss index object. It also loads the class members from a XML document. @param conjugate_gradient_document TinyXML document with the members of a conjugate gradient object.")
        .def("set_display_period", (void (ConjugateGradient::*) (const size_t&)) &ConjugateGradient::set_display_period, "Sets a new number of epochs between the training showing progress. @param Number of epochs between the training showing progress.")
		.def("set_max_epochs", (void (ConjugateGradient::*) (const size_t&)) &ConjugateGradient::set_maximum_epochs_number, "Sets a new maximum number of epochs number. @param new_maximum_epochs_number Maximum number of epochs in which the selection evalutation decreases.")
		.def("set_loss_goal", (void (ConjugateGradient::*) (const double&)) &ConjugateGradient::set_loss_goal, "Sets a new goal value for the loss. This is used as a stopping criterion when training a multilayer perceptron. @param new_loss_goal Goal value for the loss.")
		.def("set_max_time", (void (ConjugateGradient::*) (const double&)) &ConjugateGradient::set_maximum_time, "Sets a new maximum training time. @param new_maximum_time Maximum training time.")
		.def("set_minimum_loss_decrease", (void (ConjugateGradient::*) (const double&)) &ConjugateGradient::set_minimum_loss_decrease, "Sets a new minimum loss improvement during training. @param new_minimum_loss_increase Minimum improvement in the loss between two epochs.");


    // StochasticGradientDescent

    py::class_<StochasticGradientDescent> stochasticGradientDescent(m, "StochasticGradientDescent");
        
	stochasticGradientDescent.doc() = "This concrete class represents the stochastic gradient descent optimization algorithm for a loss index of a neural network. It supports momentum, learning rate decay, and Nesterov momentum.";
	
	stochasticGradientDescent.def(py::init<>(), "Default initialization method. It creates a stochastic gradient descent optimization algorithm not associated to any loss index object. It also initializes the class members to their default values.")
        .def(py::init<LossIndex*>(), "Loss index initialization method. It creates a stochastic gradient descent optimization algorithm associated to a loss index. It also initializes the class members to their default values. @param new_loss_index_pointer Pointer to a loss index object.")
        .def(py::init<const tinyxml2::XMLDocument&>(), "XML initialization method. It creates a gradient descent optimization algorithm not associated to any loss index object. It also loads the class members from a XML document. @param document TinyXML document with the members of a gradient descent object.")
        .def("set_display_period", (void (StochasticGradientDescent::*) (const size_t&)) &StochasticGradientDescent::set_display_period, "Sets a new number of epochs between the training showing progress. @param Number of epochs between the training showing progress.")
		.def("set_max_epochs", (void (StochasticGradientDescent::*) (const size_t&)) &StochasticGradientDescent::set_maximum_epochs_number, "Sets a new maximum number of epochs number. @param new_maximum_epochs_number Maximum number of epochs in which the selection evalutation decreases.")
		.def("set_loss_goal", (void (StochasticGradientDescent::*) (const double&)) &StochasticGradientDescent::set_loss_goal, "Sets a new goal value for the loss. This is used as a stopping criterion when training a multilayer perceptron. @param new_loss_goal Goal value for the loss.")
		.def("set_max_time", (void (StochasticGradientDescent::*) (const double&)) &StochasticGradientDescent::set_maximum_time, "Sets a new maximum training time. @param new_maximum_time Maximum training time.")
		.def("set_minimum_loss_increase", (void (StochasticGradientDescent::*) (const double&)) &StochasticGradientDescent::set_minimum_loss_increase, "Sets a new minimum loss improvement during training. @param new_minimum_loss_increase Minimum improvement in the loss between two iterations.");
		
		
	// LevenbergMarquardtAlgorithm

    py::class_<LevenbergMarquardtAlgorithm> levenbergMarquardtAlgorithm(m, "LevenbergMarquardtAlgorithm");
        
	levenbergMarquardtAlgorithm.doc() = "This concrete class represents a Levenberg-Marquardt Algorithm training algorithm for the sum squared error loss index for a multilayer perceptron.";
	
	levenbergMarquardtAlgorithm.def(py::init<>(), "Default initialization method. It creates a Levenberg-Marquardt optimization algorithm object not associated to any loss index object. It also initializes the class members to their default values.")
        .def(py::init<LossIndex*>(), "Loss index initialization method. It creates a Levenberg-Marquardt optimization algorithm object associated associated with a given loss index object. It also initializes the class members to their default values. @param new_loss_index_pointer Pointer to an external loss index object. ")
        .def(py::init<const tinyxml2::XMLDocument&>(), "XML initialization method. Creates a Levenberg-Marquardt algorithm object, and loads its members from a XML document. @param document TinyXML document containing the Levenberg-Marquardt algorithm data.")
        .def("set_display_period", (void (LevenbergMarquardtAlgorithm::*) (const size_t&)) &LevenbergMarquardtAlgorithm::set_display_period, "Sets a new number of epochs between the training showing progress. @param Number of epochs between the training showing progress.")
		.def("set_max_epochs", (void (LevenbergMarquardtAlgorithm::*) (const size_t&)) &LevenbergMarquardtAlgorithm::set_maximum_epochs_number, "Sets a new maximum number of epochs number. @param new_maximum_epochs_number Maximum number of epochs in which the selection evalutation decreases.")
		.def("set_loss_goal", (void (LevenbergMarquardtAlgorithm::*) (const double&)) &LevenbergMarquardtAlgorithm::set_loss_goal, "Sets a new goal value for the loss. This is used as a stopping criterion when training a multilayer perceptron. @param new_loss_goal Goal value for the loss.")
		.def("set_max_time", (void (LevenbergMarquardtAlgorithm::*) (const double&)) &LevenbergMarquardtAlgorithm::set_maximum_time, "Sets a new maximum training time. @param new_maximum_time Maximum training time.")
		.def("set_minimum_loss_decrease", (void (LevenbergMarquardtAlgorithm::*) (const double&)) &LevenbergMarquardtAlgorithm::set_minimum_loss_decrease, "Sets a new minimum loss improvement during training. @param new_minimum_loss_increase Minimum improvement in the loss between two epochs.");
}