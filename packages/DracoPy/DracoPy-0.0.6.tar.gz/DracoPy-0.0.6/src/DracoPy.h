#include<vector>
#include<cstddef>
#include "draco/mesh/triangle_soup_mesh_builder.h"
#include "draco/compression/encode.h"
#include "draco/compression/decode.h"
#include "draco/core/encoder_buffer.h"
#include "draco/core/vector_d.h"

namespace DracoFunctions {
  
  struct MeshObject {
    std::vector<float> points;
    std::vector<float> normals;
    std::vector<unsigned int> faces;

    // Encoding options stored in metadata
    bool encoding_options_set;
    int quantization_bits;
    double quantization_range;
    std::vector<double> quantization_origin;

    bool properly_decoded;
  };

  MeshObject decode_buffer(const char *buffer, std::size_t buffer_len) {
    MeshObject meshObject;
    meshObject.properly_decoded = false;
    draco::DecoderBuffer decoderBuffer;
    decoderBuffer.Init(buffer, buffer_len);
    draco::Decoder decoder;
    auto statusor = decoder.DecodeMeshFromBuffer(&decoderBuffer);
    if (!statusor.ok()) {
      return meshObject;
    }
    std::unique_ptr<draco::Mesh> in_mesh = std::move(statusor).value();
    draco::Mesh *mesh = in_mesh.get();
    const int pos_att_id = mesh->GetNamedAttributeId(draco::GeometryAttribute::POSITION);
    if (pos_att_id < 0) {
      return meshObject;
    }
    meshObject.points.reserve(3 * mesh->num_points());
    meshObject.faces.reserve(3 * mesh->num_faces());
    const auto *const pos_att = mesh->attribute(pos_att_id);
    float pos_val[3];
    for (draco::PointIndex v(0); v < mesh->num_points(); ++v) {
      pos_att->GetMappedValue(v, pos_val);
      meshObject.points.push_back(pos_val[0]);
      meshObject.points.push_back(pos_val[1]);
      meshObject.points.push_back(pos_val[2]);
    }
    for (draco::FaceIndex i(0); i < mesh->num_faces(); ++i) {
        const auto &f = mesh->face(i);
        meshObject.faces.push_back(*(reinterpret_cast<const uint32_t *>(&(f[0]))));
        meshObject.faces.push_back(*(reinterpret_cast<const uint32_t *>(&(f[1]))));
        meshObject.faces.push_back(*(reinterpret_cast<const uint32_t *>(&(f[2]))));
    }
    const draco::GeometryMetadata *metadata = mesh->GetMetadata();
    meshObject.encoding_options_set = false;
    if (metadata) {
      metadata->GetEntryInt("quantization_bits", &(meshObject.quantization_bits));
      if (metadata->GetEntryDouble("quantization_range", &(meshObject.quantization_range)) &&
          metadata->GetEntryDoubleArray("quantization_origin", &(meshObject.quantization_origin))) {
          meshObject.encoding_options_set = true;
      }
    }
    meshObject.properly_decoded = true;
    return meshObject;
  }

  std::vector<unsigned char> encode_mesh(const std::vector<float> &points, const std::vector<unsigned int> &faces,
      int quantization_bits, int compression_level, float quantization_range, const float *quantization_origin) {
    draco::TriangleSoupMeshBuilder mb;
    mb.Start(faces.size());
    const int pos_att_id =
      mb.AddAttribute(draco::GeometryAttribute::POSITION, 3, draco::DataType::DT_FLOAT32);

    for (std::size_t i = 0; i <= faces.size() - 3; i += 3) {
      auto point1Index = faces[i]*3;
      auto point2Index = faces[i+1]*3;
      auto point3Index = faces[i+2]*3;
      mb.SetAttributeValuesForFace(pos_att_id, draco::FaceIndex(i), draco::Vector3f(points[point1Index], points[point1Index+1], points[point1Index+2]).data(), draco::Vector3f(points[point2Index], points[point2Index+1], points[point2Index+2]).data(), draco::Vector3f(points[point3Index], points[point3Index+1], points[point3Index+2]).data());  
    }

    std::unique_ptr<draco::Mesh> ptr_mesh = mb.Finalize();
    draco::Mesh *mesh = ptr_mesh.get();
    draco::Encoder encoder;
    int speed = 10 - compression_level;
    encoder.SetSpeedOptions(speed, speed);
    std::unique_ptr<draco::GeometryMetadata> metadata = std::unique_ptr<draco::GeometryMetadata>(new draco::GeometryMetadata());
    metadata->AddEntryInt("quantization_bits", quantization_bits);
    if (quantization_origin == NULL || quantization_range == -1) {
      encoder.SetAttributeQuantization(draco::GeometryAttribute::POSITION, quantization_bits);
    } 
    else {
      encoder.SetAttributeExplicitQuantization(draco::GeometryAttribute::POSITION, quantization_bits, 3, quantization_origin, quantization_range);
      metadata->AddEntryDouble("quantization_range", quantization_range);
      std::vector<double> quantization_origin_vec;
      for (int i = 0; i < 3; i++) {
        quantization_origin_vec.push_back(quantization_origin[i]);
      }
      metadata->AddEntryDoubleArray("quantization_origin", quantization_origin_vec);
    }
    mesh->AddMetadata(std::move(metadata));
    draco::EncoderBuffer buffer;
    const draco::Status status = encoder.EncodeMeshToBuffer(*mesh, &buffer);
    return *((std::vector<unsigned char> *)buffer.buffer());
  }
}
