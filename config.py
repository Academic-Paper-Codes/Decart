# decart/config.py
"""
DeCart configuration file.
Defines system parameters and constants.
"""

import os
from typing import Optional

class Config:
    """Configuration class storing all system parameters."""
    
    # ========== Security Parameters ==========
    SECURITY_PARAMETER: int = 256  # lambda - security parameter
    
    # ========== Bilinear Pairing Parameters ==========
    CURVE_TYPE: str = "bls12_381"  # Elliptic curve type in use
    
    # ========== System Capacity Parameters ==========
    MAX_USERS: int = 10000     # N: maximum number of users supported
    BLOCK_SIZE: int = 32       # n: number of users in each block
    NUM_BLOCKS: Optional[int] = None  # B: total number of blocks, computed at initialization
    
    # ========== Homomorphic Encryption Parameters ==========
    HOMOMORPHIC_SCHEME: str = "CKKS"  # Homomorphic encryption scheme in use
    
    # CKKS-specific parameters
    POLY_MODULUS_DEGREE: int = 32768    # Polynomial modulus degree
    COEFF_MOD_BIT_SIZES: list = [60, 40, 40, 60]  # Coefficient modulus bit sizes
    SCALE: int = 2**40                   # Scaling factor

    # ========== Default Experiment Parameters ==========
    EXPERIMENT_NUM_RECORDS: int = 32
    EXPERIMENT_RECORD_DIM: int = 32
    EXPERIMENT_POLICY_SIZE: int = 32
    EXPERIMENT_NUM_RUNS: int = 3
    EXPERIMENT_FIXED_DATA_SIZE: int = 100
    EXPERIMENT_REGISTER_N_VALUES: tuple = (100, 1000)
    
    # ========== Database Configuration ==========
    DATABASE_SERVERS: int = 3           # Number of database servers
    THRESHOLD_SERVERS: int = 2          # Minimum servers required for decryption
    
    # ========== Hash Function Configuration ==========
    HASH_ALGORITHM: str = "sha256"      # Hash algorithm in use
    HASH_OUTPUT_SIZE: int = 32          # Hash output size (bytes)
    
    # ========== File Path Configuration ==========
    DATA_DIR: str = "data"              # Data storage directory
    KEYS_DIR: str = "keys"              # Key storage directory
    LOGS_DIR: str = "logs"              # Log storage directory
    
    # ========== Performance Parameters ==========
    USE_PARALLEL: bool = False          # Whether to use parallel computation
    BATCH_SIZE: int = 100               # Batch size
    
    @classmethod
    def initialize(cls):
        """Initialize configuration parameters."""
        print("Initializing DeCart configuration...")
        
        # Compute number of blocks B = ceil(N / n)
        cls.NUM_BLOCKS = (cls.MAX_USERS + cls.BLOCK_SIZE - 1) // cls.BLOCK_SIZE
        
        # Create required directories
        dirs_to_create = [cls.DATA_DIR, cls.KEYS_DIR, cls.LOGS_DIR]
        for directory in dirs_to_create:
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")
        
        # Print configuration
        cls.print_config()
    
    @classmethod
    def print_config(cls):
        """Print current configuration."""
        print("\n" + "="*50)
        print("DeCart System Configuration")
        print("="*50)
        print(f"Security Parameter (lambda): {cls.SECURITY_PARAMETER}")
        print(f"Maximum Users (N): {cls.MAX_USERS}")
        print(f"Block Size (n): {cls.BLOCK_SIZE}")
        print(f"Total Blocks (B): {cls.NUM_BLOCKS}")
        print(f"Bilinear Curve: {cls.CURVE_TYPE}")
        print(f"Homomorphic Scheme: {cls.HOMOMORPHIC_SCHEME}")
        print(f"Database Servers: {cls.DATABASE_SERVERS}")
        print(f"Decryption Threshold: {cls.THRESHOLD_SERVERS}")
        print("="*50)
    
    @classmethod
    def update_parameters(cls, 
                         max_users: Optional[int] = None,
                         block_size: Optional[int] = None,
                         security_param: Optional[int] = None):
        """Update system parameters."""
        if max_users is not None:
            cls.MAX_USERS = max_users
        
        if block_size is not None:
            cls.BLOCK_SIZE = block_size
        
        if security_param is not None:
            cls.SECURITY_PARAMETER = security_param
        
        # Recompute number of blocks
        cls.NUM_BLOCKS = (cls.MAX_USERS + cls.BLOCK_SIZE - 1) // cls.BLOCK_SIZE
        
        print("Parameters updated")
        cls.print_config()
    
    @classmethod
    def get_prime_order(cls) -> int:
        """Get the finite field prime order p (mock value for testing)."""
        # Returns a large random prime for testing purposes.
        # In production, p should come from the bilinear pairing library.
        import sympy
        return sympy.randprime(2**254, 2**256 - 1)
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration correctness."""
        try:
            # Validate basic parameters
            assert cls.SECURITY_PARAMETER >= 128, "Security parameter must be at least 128 bits"
            assert cls.MAX_USERS > 0, "Maximum users must be positive"
            assert cls.BLOCK_SIZE > 0, "Block size must be positive"
            assert cls.BLOCK_SIZE <= cls.MAX_USERS, "Block size cannot exceed maximum users"
            assert cls.DATABASE_SERVERS > 0, "At least one database server is required"
            assert cls.THRESHOLD_SERVERS > 0, "Threshold must be positive"
            assert cls.THRESHOLD_SERVERS <= cls.DATABASE_SERVERS, "Threshold cannot exceed number of servers"
            
            # Validate homomorphic encryption parameters
            if cls.HOMOMORPHIC_SCHEME == "CKKS":
                valid_poly_modulus = [1024, 2048, 4096, 8192, 16384, 32768]
                assert cls.POLY_MODULUS_DEGREE in valid_poly_modulus, f"Polynomial modulus degree must be one of {valid_poly_modulus}"
                assert cls.SCALE > 0, "Scale must be positive"
            
            print("Configuration validation passed")
            return True
            
        except AssertionError as e:
            print(f"Configuration validation failed: {e}")
            return False


# Test function
def test_config():
    """Test the configuration module."""
    print("Testing configuration module...")
    
    # Create config reference
    config = Config
    
    # Test initialization
    config.initialize()
    
    # Test parameter update
    config.update_parameters(max_users=500, block_size=20)
    
    # Test validation
    is_valid = config.validate_config()
    
    # Test getting prime order (mock)
    prime_order = config.get_prime_order()
    print(f"Generated prime order (p): {prime_order}")
    print(f"Prime bit length: {prime_order.bit_length()}")
    
    # Test directory creation
    import os
    for directory in [config.DATA_DIR, config.KEYS_DIR, config.LOGS_DIR]:
        assert os.path.exists(directory), f"Directory {directory} does not exist"
        print(f"Directory exists: {directory}")
    
    print("\nConfiguration module test completed")
    return True


if __name__ == "__main__":
    # Run test
    success = test_config()
    if success:
        print("\nConfiguration module is ready for use")
    else:
        print("\nConfiguration module test failed")