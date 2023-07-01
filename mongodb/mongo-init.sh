set -e

mongosh <<EOF

use ${DB_NAME}

db.createCollection(${COLLECTION_NAME})

EOF
